# Preflight Energy Consumption Prediction for Delivery UAVs Using Flight Planning Parameters

DTA301 Project Team  |  FPT University

### Abstract

Accurate flight energy estimates can support battery planning for small delivery drones. This study evaluates whether total recorded flight energy can be predicted using three parameters available before takeoff: commanded speed, payload, and commanded altitude. Voltage and current telemetry from a public quadcopter dataset are integrated with the trapezoidal rule using actual sampling intervals. Explicit exclusion rules retain 192 of 209 flights. Linear regression and ridge baselines are compared with regression including squared speed, random forests, and gradient boosting. Evaluation uses five fold cross validation repeated ten times; tree model hyperparameters are selected inside each training fold. Regression with squared speed achieves a mean absolute error of 0.849 Wh, a root mean squared error of 1.375 Wh, and a mean coefficient of determination of 0.908. Its mean absolute error is 42.5% lower than the linear baseline. Gradient boosting has a slightly lower mean absolute error, but the corrected paired comparison does not detect a significant difference. Boundary holdout experiments favor squared speed regression in three of four tested settings. All models systematically underestimate five flights on the longer R6 route, exposing the limitation of omitting route length. The results support compact, interpretable energy prediction within the observed flight conditions; they do not establish operational flight authorization or reliability on unseen routes.

Keywords: UAV energy prediction; preflight planning; polynomial regression; cross validation; delivery drones.

## I Introduction

A delivery drone must carry enough usable energy to complete its intended flight. Estimating consumption before takeoff requires a distinction between planned operating settings and telemetry that becomes available only during the flight. A model that uses measured flight duration or mean electrical power as an input may appear accurate while being unsuitable for the planning stage. We therefore formulate a flight level regression problem with energy in watt hours as the target and only commanded speed, payload mass, and commanded altitude as the primary predictors.

Rodrigues et al. published positional and electrical measurements for 209 flights of a DJI Matrice 100 [1], with the underlying data available through KiltHub [2]. Subsequent work developed an empirical, physics motivated energy model and examined delivery energy and emissions [3]. Our analysis uses the same public experimental resource for a narrower comparison of compact regression and tree ensembles. It neither reproduces that paper’s physical model nor compares numerical accuracy directly, because data selection, inputs, and evaluation protocols differ.

The research question is whether adding a simple nonlinear speed term can improve flight energy prediction while retaining interpretability. The analysis combines an auditable energy target, common validation splits, residual diagnostics, and boundary holdouts. Route specific failures are examined alongside aggregate accuracy so that a low average error is not mistaken for dependable performance on every flight.

## II Methodology

### A Data and flight selection

The local data consist of parameters.csv with 209 rows and seven columns, and flights.csv with 257,896 telemetry rows and 28 columns. Both contain the same 209 flight identifiers. The parameter file defines the operating settings; the telemetry file supplies timestamps, voltage, current, position, velocity, and other measurements. The primary experimental ranges are 4–12 m/s commanded speed, 0–500 g payload, and 25–100 m commanded altitude. The three retained payload levels are 0, 250, and 500 g, rather than five evenly spaced levels.

TABLE I  Flight exclusion rules

| Rule | Flights removed | Rationale |
| --- | --- | --- |
| Stationary and hover tests | 13 | Commanded speed is zero |
| Changing altitude within flight | 2 | R7 has no single altitude setting |
| Payload outside study range | 1 | Only one flight at 750 g |
| Extended recording after landing | 1 | Flight 196 contains a long idle tail |
| Retained flights | 192 | 209 minus 17 exclusions |

These are study inclusion rules, not claims that all excluded measurements are invalid. In particular, flight 196 is removed by the existing pipeline rather than trimmed. This limits the target to the retained recordings and should be revisited in a sensitivity analysis. No missing values or duplicate rows are found in either input file. Altitude is converted from text to a numeric value after the changing altitude flights are removed. Each retained flight contributes exactly one modeling row.

### B Energy target construction

For sample j in flight i, electrical power is Pᵢⱼ = Vᵢⱼ Iᵢⱼ. Flight energy is integrated over the complete retained recording using actual elapsed time and the trapezoidal rule:

Eᵢ = (1/3600) ∑ⱼ₌₂ⁿᵢ [(Pᵢ,ⱼ₋₁ + Pᵢⱼ)/2] (tᵢⱼ − tᵢ,ⱼ₋₁)     (1)

Voltage is in volts, current in amperes, and time in seconds; division by 3600 converts joules to watt hours. Sampling intervals average 0.15025 s and range from 0.06 to 5.28 s over the raw records. Intervals are positive but unequal. The pipeline keeps small negative current readings and bridges retained gaps by trapezoidal integration; it does not reconstruct unobserved power within a gap. A left Riemann comparison differs by 0.051% on average and at most 0.247% over the retained flights. Agreement between integration rules is a numerical check, not an independent calibration of the sensors.

![energy_EN.png](work/assets/energy_EN.png)

Fig. 1. Electrical power over flight 1. The integrated area corresponds to 21.766 Wh.

### C Predictors and model configurations

The primary input vector is x = [v, m, h], where v is commanded horizontal speed in m/s, m is payload in grams, and h is commanded altitude in meters. These are planned settings, not measured flight averages. Recorded duration, mean power, maximum power, and measured velocity are excluded from the predictor matrix. Wind telemetry is also excluded because the current data flow does not provide a forecast available at prediction time. Battery state of charge and state of health are not inputs in the implemented models.

TABLE II  Implemented model configurations

| Model | Configuration |
| --- | --- |
| B0 Mean | Training fold mean; no predictors |
| B1 Distance | Linear regression on route median GPS path length |
| B2 Linear | Ordinary least squares using v, m, h |
| B3 Ridge | v, m, h; alpha = 1; no scaling |
| M1 Squared speed | Ordinary least squares using v, m, h, v² |
| M2 Random Forest | 200 trees; min_samples_leaf in {1, 3, 5} |
| M3 Gradient Boosting | 200 stages; learning_rate = 0.05; max_depth in {1, 2, 3} |

An additional B2 plus distance model is exploratory. Distance is reconstructed by summing horizontal GPS increments and assigning each route its median recorded path length. This is an observed route proxy computed before splitting, rather than independently supplied mission geometry. It is not an input to the main M1–M3 comparison. All estimators use scikit-learn [4]; settings not listed in Table II retain their implementation defaults.

### D Validation and evaluation metrics

RepeatedKFold uses five folds, ten repetitions, and random_state = 301 [6]. Each outer split trains on 153 or 154 flights and evaluates 39 or 38 flights, respectively. The same 50 outer splits are used by all primary models. Each flight is held out once per repetition, and no telemetry row from that flight enters training because aggregation precedes splitting. These are random flight splits; routes, dates, and repeated operating settings can occur in both sets.

For M2 and M3, GridSearchCV selects hyperparameters using shuffled five fold validation inside each outer training set, with seed 301 and negative mean absolute error as the selection score [6]. M1 uses a deterministic squared speed transformation followed by linear regression and requires no tuning grid. Mean absolute error (MAE), root mean squared error (RMSE), and the coefficient of determination (R²) are computed on each outer held out set:

MAE = mean(|y − ŷ|);  RMSE = √mean((y − ŷ)²)     (2)

R² = 1 − ∑(y − ŷ)² / ∑(y − mean(y))²     (3)

Tables report the mean and population standard deviation across 50 scores, matching the implementation. For diagnostic plots only, ten held out predictions per flight are averaged. Metrics from those averaged predictions are not substituted for the fold level results. MAE divided by mean target energy is a normalization, not mean absolute percentage error.

## III Results

### A Exploratory data analysis

The retained target has a mean of 21.27 Wh, standard deviation of 4.90 Wh, median of 20.79 Wh, and range of 12.99–37.75 Wh. Route R1 accounts for 180 of 192 flights (93.75%). The remaining flights comprise one each on R2, R3, and R4, four on R5, and five on R6. This concentration is important: overall validation accuracy primarily reflects conditions represented by R1.

![eda_EN.png](work/assets/eda_EN.png)

Fig. 2. Recorded flight energy versus each primary predictor. Dots represent flights; black lines connect group means. Horizontal jitter improves visibility and does not change the recorded settings.

TABLE III  Mean energy and sample counts by operating setting

| Predictor | Setting levels | Mean energy Wh | Flight counts |
| --- | --- | --- | --- |
| Speed m/s | 4 / 6 / 8 / 10 / 12 | 27.0 / 22.1 / 19.8 / 18.6 / 18.6 | 40 / 38 / 36 / 41 / 37 |
| Payload g | 0 / 250 / 500 | 19.2 / 21.5 / 23.1 | 66 / 61 / 65 |
| Altitude m | 25 / 50 / 75 / 100 | 17.4 / 20.5 / 22.6 / 25.2 | 53 / 47 / 47 / 45 |

Mean energy decreases sharply from 4 to 8 m/s and changes little between 10 and 12 m/s. In contrast, payload and altitude show approximately increasing trends. These are marginal summaries: each group still contains variation in the other settings and in route. The plots therefore describe associations in this dataset and do not isolate a causal effect of changing one parameter.

EDA also computes the 90th percentile of measured horizontal speed within each flight. Averaging that diagnostic by commanded speed gives approximately 9.65 m/s at a 10 m/s command and 10.66 m/s at a 12 m/s command. This is consistent with diminishing benefit from the highest command, but does not prove a universal physical optimum. Measured speed remains a diagnostic rather than a predictor. Flight duration correlates strongly with energy (r = 0.83), yet is excluded because its realized value is unavailable before takeoff.

ANOVA and Kruskal–Wallis checks in the EDA notebook both report p < 0.001 for differences between groups of each primary predictor. These exploratory checks support further modeling; shared operating conditions and multiple comparisons limit an independent causal interpretation. The curved speed trend motivates M1, while the increasing payload and altitude patterns motivate retaining their linear terms.

### B Predictive performance

TABLE IV  Repeated cross validation results mean ± standard deviation

| Model | MAE Wh | RMSE Wh | R² |
| --- | --- | --- | --- |
| B0 | 3.979 ± 0.432 | 4.903 ± 0.523 | -0.058 ± 0.112 |
| B1* | 4.007 ± 0.454 | 4.946 ± 0.532 | -0.077 ± 0.128 |
| B2 | 1.478 ± 0.168 | 1.937 ± 0.462 | 0.829 ± 0.072 |
| B3 | 1.478 ± 0.168 | 1.937 ± 0.462 | 0.829 ± 0.072 |
| B2 + distance* | 1.362 ± 0.106 | 1.675 ± 0.206 | 0.874 ± 0.030 |
| M1 | 0.849 ± 0.172 | 1.375 ± 0.549 | 0.908 ± 0.067 |
| M2 | 0.882 ± 0.212 | 1.537 ± 0.559 | 0.885 ± 0.077 |
| M3 | 0.833 ± 0.188 | 1.409 ± 0.548 | 0.903 ± 0.067 |

* Distance variants are exploratory and use route proxies reconstructed before cross validation. Their evaluation is not an independent test of planned distance on a new route.

M1 reduces mean MAE from 1.4782 Wh for B2 to 0.8494 Wh, a 42.5% reduction. Its RMSE is 1.3755 Wh and mean R² is 0.9078. M3 has the lowest MAE at 0.8329 Wh; M1 has the lowest RMSE and highest mean R² among the three new models. M2 reaches 0.8818 Wh MAE. The ratio of M1 MAE to the dataset’s mean energy is approximately 4.0%; this is not a guarantee that each flight is within 4%.

![oof_EN.png](work/assets/oof_EN.png)

Fig. 3. M1 diagnostics using the mean of ten out of fold predictions per flight. Left: actual versus predicted energy with the identity line. Right: residual versus predicted energy; positive residuals indicate underprediction. R6 is highlighted.

Ridge and unregularized linear regression have almost identical errors in this configuration. This observation does not establish that regularization is generally unnecessary: alpha is fixed at 1 and inputs are not standardized. In the nested searches, random forest selects min_samples_leaf = 1 in all 50 outer fits, while gradient boosting selects max_depth = 2 in 45 fits and 3 in five fits.

### C Paired comparisons and error analysis

The implementation compares paired outer fold MAEs using a corrected t statistic motivated by Nadeau and Bengio [5]. For K = 50 differences d and sample variance s², it uses t = mean(d) / sqrt[(1/K + n_test/n_train)s²], with 49 degrees of freedom. The size ratio is taken from the first split (39/153). This is an approximate dependence correction; the p values are unadjusted for multiple pairwise comparisons.

TABLE V  Corrected paired MAE comparisons

| Difference | Mean difference Wh | p value |
| --- | --- | --- |
| B2 − M1 | 0.629 | 2.56e-12 |
| B2 − M2 | 0.596 | 1.97e-08 |
| B2 − M3 | 0.645 | 2.57e-11 |
| M1 − M3 | 0.017 | 7.89e-01 |
| M1 − M2 | -0.032 | 6.93e-01 |

All three new models improve over B2 on every one of the 50 splits, with corrected p < 0.001. For M1 versus M3, p ≈ 0.79; for M1 versus M2, p ≈ 0.69. These comparisons do not provide evidence of different mean MAEs under this protocol. They do not demonstrate equivalence, and should not be interpreted as proof that the methods have identical performance.

Using the averaged held out predictions, B2 underestimates 26 flights by more than 2 Wh; M1, M2, and M3 each reduce that count to seven. Five of those seven are the five R6 flights. M1 has MAE 0.69 Wh on R1–R5 but 6.71 Wh on R6. Flight 272, the highest energy flight at 37.75 Wh, remains severely underestimated. The reduction in average error therefore leaves a concentrated failure mode unresolved.

### D Boundary holdout experiments

A separate stress test removes all flights at one boundary speed or altitude, fits each model on the remaining flights, and evaluates the omitted level. Tree hyperparameters are selected within the remaining training data. This tests four specific missing settings; it is not the same protocol as the 50 fold scores and is not a test of new routes.

TABLE VI  MAE in Wh on the omitted setting

| Omitted level | B2 | M1 | M2 | M3 |
| --- | --- | --- | --- | --- |
| Speed 4 m/s | 4.34 | 1.66 | 5.02 | 4.99 |
| Speed 12 m/s | 3.43 | 1.71 | 0.85 | 0.78 |
| Altitude 25 m | 1.76 | 1.25 | 3.19 | 3.20 |
| Altitude 100 m | 1.31 | 0.84 | 2.50 | 2.72 |

M1 has the lowest error in three cases, whereas M3 performs best when 12 m/s is withheld. The limited increase in realized speed between the 10 and 12 m/s commands is consistent with that exception. These results favor M1 as a compact model for the tested boundaries, without establishing safe extrapolation beyond the experimental ranges.

## IV Discussion

### A Model choice and interpretation

We select M1 because it substantially improves over the linear baseline, has competitive aggregate scores, exposes its predictor effects directly, and performs well in three tested boundary holdouts. This choice balances the evidence rather than treating the lowest MAE as the only objective. Its full data fit is:

Ê = 32.1960 − 4.1944v + 0.1969v² + 0.0081m + 0.1050h     (4)

Here energy is in Wh, speed in m/s, payload in g, and altitude in m. The coefficients are rounded for presentation. Equation (4) is fitted on all 192 flights for interpretation; validation results come from separate fits within the folds. It is not an additional independent evaluation, nor a serialized deployment artifact. Holding the other inputs fixed, the fitted payload coefficient corresponds to about 0.81 Wh per extra 100 g and the altitude coefficient to 2.63 Wh per extra 25 m.

The positive squared speed term corrects the curved residual pattern of B2. The fitted parabola has its minimum near 10.7 m/s. That value is descriptive of the current fit and commanded speed range. It should not be presented as an operational optimum: unmodeled route length, weather, battery condition, speed tracking, and prediction uncertainty can change the planning decision. Likewise, coefficient signs and group trends do not establish causal effects.

### B Route length and information availability

The GPS analysis finds median horizontal path lengths of about 472 m on R1 and 837 m on R6, with R2–R5 route medians between about 427 and 534 m. These are sums of recorded horizontal movement, not confirmed one way delivery distances. They cannot automatically be doubled into a return mission or used to claim a tested delivery range. Without distance, identical v, m, and h produce the same prediction even when routes differ substantially. This structural limitation explains why a more flexible learner alone cannot resolve the R6 errors.

Adding the route distance proxy to B2 reduces repeated validation MAE from 1.4782 to 1.3621 Wh. The single five fold diagnostic in notebook 03 also reduces R6 MAE from approximately 6.85 to 2.8 Wh. However, the proxy is derived from all flights of each route before validation. For routes represented by one flight, it is that flight’s observed path length. No target energy is used to construct it, but the procedure still does not represent a clean, independent preflight input evaluation. Planned route geometry, or a proxy fitted on training data alone, is needed for a stronger claim.

### C Limits of the current evidence

Random flight cross validation measures performance within the available collection. It does not hold out complete routes, dates, or operating configurations, and no external dataset is tested. Inclusion rules and the decision to add squared speed were informed by exploration of this same collection. Nested tuning controls tree hyperparameter selection, but does not remove all optimism from choosing the overall model family after examining results. The retained R6 sample has only five flights, so route specific estimates are uncertain.

Neither low MAE nor favorable boundary errors establish flight safety. No implemented decision function combines usable battery capacity, an outbound and return mission, a 20% reserve, or a 25% charge threshold. The baseline notebook’s analytical prediction interval is based on linear assumptions and an approximate coverage check; it is not a calibrated interval for M1. An independently validated uncertainty model and explicit battery assumptions are prerequisites for a future Fly or No fly layer.

## V Conclusion

For the retained 192 flights, a regression model with commanded speed, squared speed, payload, and commanded altitude achieves MAE 0.849 Wh, RMSE 1.375 Wh, and mean R² 0.908 under five fold cross validation repeated ten times. Adding the squared speed term reduces MAE by 42.5% relative to the linear baseline. Its error is competitive with tuned tree ensembles, and it performs best in three of four boundary holdouts. These findings support a small, interpretable model for energy prediction under conditions represented by the dataset.

The persistent underprediction of all five R6 flights is the principal unresolved limitation. Future work should supply independently known planned distance, evaluate route and date holdouts, quantify prediction uncertainty, and test sensitivity to recording boundaries and exclusion rules. Battery condition, weather forecasts, and return flight requirements require explicit data and validation before energy predictions can support operational flight decisions.

### Reproducibility

The analysis is implemented in four ordered notebooks for cleaning, EDA, baselines, and experiments. Random operations use seed 301. The full main experiment, baselines, and boundary holdouts were rerun for this manuscript; results matched the stored tables to their reported precision. The energy target was independently recalculated from raw voltage, current, and elapsed time. The verification environment used Python 3.11.9, NumPy 2.4.6, pandas 3.0.3, SciPy 1.17.1, and scikit-learn 1.9.1. Diagnostic figures use the same data and split protocol; no additional predictive inputs are introduced.

### References

[1] T. A. Rodrigues et al., “In-flight positional and energy use data set of a DJI Matrice 100 quadcopter for small package delivery,” Scientific Data, vol. 8, art. 155, 2021, doi: 10.1038/s41597-021-00930-x. https://arxiv.org/abs/2103.13313

[2] T. A. Rodrigues et al., “Data Collected with Package Delivery Quadcopter Drone,” KiltHub, dataset, doi: 10.1184/R1/12683453. https://doi.org/10.1184/R1/12683453

[3] T. A. Rodrigues, J. Patrikar, N. L. Oliveira, H. S. Matthews, S. Scherer, and C. Samaras, “Drone flight data reveal energy and greenhouse gas emissions savings for very small package delivery,” Patterns, vol. 3, no. 8, art. 100569, 2022, doi: 10.1016/j.patter.2022.100569.

[4] F. Pedregosa et al., “Scikit-learn: Machine Learning in Python,” Journal of Machine Learning Research, vol. 12, pp. 2825–2830, 2011. https://jmlr.org/papers/v12/pedregosa11a.html

[5] C. Nadeau and Y. Bengio, “Inference for the Generalization Error,” Machine Learning, vol. 52, pp. 239–281, 2003, doi: 10.1023/A:1024068626366.

[6] Scikit-learn developers, “RepeatedKFold” and “GridSearchCV,” API documentation, accessed Nov. 3, 2026. https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.RepeatedKFold.html ; https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html

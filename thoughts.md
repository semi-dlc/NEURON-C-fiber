#### Word to Markdown conversion with LLM.

## Values from paper
For variables ["CV", "0to025", "025to2", "30sRecovery", "50%RecoveryTime"]:
CMi:
experiment_values_covid = [0.52, 5.52, 31.8, 31.6, 62.2]
experiment_values_healthy = [0.43, 4.09, 36, 19.7, 96.2]
experiment_factors = [1.20930233, 1.34963325, 0.88333333, 1.60406091, 0.64656965]

CM:
experiment_values_covid = [0.67, 0.01, 32.8, 33.6, 46.65]
experiment_values_healthy = [0.72, 0.16, 25.95, 38.95, 37]
experiment_factors =  [0.93055556, 0.0625    , 1.26396917, 0.86264442, 1.26081081]

### Changes of less than 1% are ignored in the section beneath.
For CMi/Type 1B:
1. Can be increased to 1.209 partially by increasing gNav17, gNav18, decreasing gKdr, gH, gKf, 
2. Can be increased to 1.349 fully by decreasing gPump by 10%, additionally by increasing gNav18, gKdr, gKNa,
3. Can be decreased to 0.8833 fully through a combination of increasing gPump, increasing gNav17, gKs, decreasing gH, gKdr, gKna
4. Can be increased to 1.604 partially through a combination of decreasing gPump, gNav17, increasing gNav18, decreasing gKs, increasing gKdr, gKna. Total explanation is probably possible by changing the conductances more strongly.
5. Can be decreased to 0.6466 partially through a combination of increasing gNav18, decreasing gNav19, increasing gKs, gH, gKdr,

For CM/Type 1A:
1. Can be decreased to 0.93055556 through a combination of decreasing gNav17, gNav18, 
2. Can be decreased to 0.0625  partially through a combination of increasing gPump, decreasing gNav18, increasing gKs, decreasing gKf, increasing gH, decreasing gKdr, gKna. For this value, the covid value is very low. Would it make sense to use the ratio even here?
3. Can be increased to 1.264 fully through a combination of decreasing gPump, decreasing gNav17, increasing gNav18, decreasing gKs, gH, increasing gKdr, increasing gKna
4. Can be decreased to 0.863 fully by increasing gPump, decreasing gNav18, increasing gKs, decreasing gKf, increasing gH, decreasing gKdr, decreasing gKna by 5%.
5. Can be increased to 1.261 fully through a combination of decreasing gPump, gKs, and perhaps by increasing gKdr partially.

## Pending: Conclusion which channels are involved now.

## Influence of Conductances on Latency

| Conductance | Effect on Latency |
|---|---|
| gPump | Strongly negative |
| gNav17 | Slightly negative |
| gNav18 | Positive |
| gNav19 | Barely |
| gKs | Negative |
| gKf | Barely |
| gH | Positive |
| gKdr | Strongly positive |
| gKna | Positive |

> Is this explainable through the sensitivity analysis of Tigerholm 2014, Fig. A3? Question: If one conductance plays a big role in the spike process, does increasing the conductance increase the sensitivity w.r.t this conductance?

## Effect of Conductances on Metrics (Ribeiro 2025)

| Conductance | Slowing 0–0.25 Hz | Slowing 0.25–0.5 Hz | Recovery at 30s | Time to 50% Recovery |
|---|---|---|---|---|
| gPump | Negative | Positive | Negative | Negative |
| gNav17 | Inconclusive | Inconclusive | Inconclusive | Inconclusive |
| gNav18 | Rather negative | Negative | Negative | Inconclusive |
| gNav19 | Rather positive | Inconclusive | Inconclusive | Inconclusive |
| gKs | Rather negative | Rather positive | Inconclusive | Inconclusive |
| gKf | Inconclusive | Rather negative | Rather negative | Inconclusive |
| gH | Rather positive | Rather negative | Rather negative | Inconclusive |
| gKdr | Inconclusive | Inconclusive | Inconclusive | Inconclusive |
| gKna | Inconclusive | Rather positive | Positive | Inconclusive |

## Open Questions 

- Time to 50% recovery may not be explainable through the HH framework
- Optimization approach: Bayesian optimization preferred over Simulated Annealing due to fewer required evaluations
- Optimization problem is underconstrained: 8 free parameters vs. 4 target values
- Consider dropping gNav17, gNav19, and gKdr to focus on the more influential variables
- If one conductance plays a big role in the spike process, does increasing the conductance increase the sensitivity w.r.t this conductance?
- Is it expected that the relations are so nonlinear? Intuitively, if the HH system is strongly nonlinear, the relations could be nonlinear as well. Especially gKf, gNav19, gNav17 have weird shapes. In the meanwhile, currents that are important for ADS (gNav18), seem to have good scaling.
- Can the conductances be treated as independent from each other in the influence onto the ADS recovery? -> We assume so for now to study the effect that each conductance has onto the ADS recovery.
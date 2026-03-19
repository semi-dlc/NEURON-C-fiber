## Problem with finding channels which explain the change:
Problematic:
- The two different models show similar behavior when changing the channel conductances
- Which is expected since only the parameters change, but not the equations themselves
- All changes in the metrics are more or less linear wrt change in conductance in CM, but CMi has more nonlinearities. For vRest, both are nonlinear, with maximum close to dg = 0
- Therefore, it is hard to find a single parameter, or multiple parameters, that could explain all the changes (because CM/CMi recording went in opposite directions)
- no speeding observed for all parameter changes.

## Brute-force finding channels: notes for thinking
vRest is ignored for now as it mainly decreases all metrics when deviated in both directions.
CMi:
- gNav18 +30% explains 1, 2, 3, 5. 4 is not affected a lot. 1 is only partially explained.
- Which channels affect 4?:
    - Decrease gPump, which is good for 2, and 3 (if between -60% - -40%), but is undefined for 5
    - Decrease gNav17 by around -40%, which is strongly bad for 1 (effect is stronger than increase of gNav18 on 1), good for 2, strongly bad for 3, and good for 5. We should not consider it because it is so bad on 1 and 3.
    - Increase gNav19: Has little effect, we should not consider this atm.
    - Decrease gKs by around -20%, which barely affects 1 and 3, is good for 2, and is bad for 5.
    - Increase gKdr: Is bad for 1, good for 2, bad for 3, good for 4, good for 5.
    - Increase gKNa: Does not change 1, good for 2, good for 3 (when excessive ~80%), good for 4, bad for 5 (metric undefined for increasing)
- -> Decreasing gKs is good if we can compensate 5 somehow. We could try increasing gNav17 in the meanwhile so 1 is compensated. gNav17 affects 2 less strong than gNav18. However, increasing gNav17 worsens 5, and gNav18 does not affect 5 enough to compensate for the errors of gKs and gNav17 in 5.
- -> If we ignore 5, a combination of increasing gNav18, decreasing gKs, and potentially increasing gNav17 would be able to explain it.
- if we increase gH also, gH could explain 5 while not affecting 1-4 a lot.
- if we increase gKdr slightly (~20%), 2, 4, 5 are more correct but 3 is strongly off, and 1 is slightly off.
- -> try combinations of increasing gNav18, decreasing gKs, increasing gNav17, and increasing gH or gKdr.  

CM:
- Metric 1: decrease gNav17, decrease gNav18 slightly, increase gH, increase gKdr
- decrease gNav17 ~-40%: Explains 1, does not change 2, explains 3 partially, is bad for 4, does not change 5 -> look at 2, 4, 5
- decrease gNav18 ~-30%: Explains 1, explains 2, is bad for 3 (stronger than gNav17), explains 4 (stronger than gNav17), barely affects 5 -> Look at 3, 5.  
- 5 can be explained by:
    - decreasing gPump
    - decreasing gKs (but the metric is undefined for <-20%)
    - decreasing gH (partially)
    - increasing gKna (but the metric is undefined for >20%)
- 3 can be explained by:
    - decreasing gPump
    - decreasing gKs (~-20%) 
    - decreasing gH
    - increasing gKdr
    - increasing gKNa
- these are basically the same channels -> which one affects the other ones the least?:
    - 1 is ok for basically all
    - 2 is not strongly affected by decreasing gH -> let's look at gH
    - gH would influence 4 negatively (roughly the same as gNav18 influences 4 positively), influence 1 negatively (but compensated by gNav17, gNav18), influence 2 negatively (but compensated by gNav18)
- -> try combinations of  decreasing gNav17, gNav18, and decreasing gH
- 5 is still not well-explained
- -> right now 5 can be explained a bit, but 4 not at all -> decrease effect of gH again? But then other metrics fail again.
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

## add: make timeto50% percentage of percentage

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
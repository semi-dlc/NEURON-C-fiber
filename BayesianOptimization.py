import neuron as neuron
from dataProcessing import getData, getFilename, calculateLatency, calculateVelocity
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from stimulationProtocols import getCOVIDFullTime
from plot import plotLatency, plotRecoveryCycle, getLatency
import os
from skopt import Optimizer
from skopt.space import Real
from joblib import Parallel, delayed, parallel_config
from main import run

neuron.load_mechanisms('./MOD_Tigerholm')

gPump = -0.0047891
gNav17 = 0.10664
gNav18 = 0.24271
gNav19 = 9.4779e-05
gKs = 0.0069733
gKf = 0.012756
gH = 0.0025377
gKdr = 0.018002
gKna = 0.00042
vRest = -55

param_orig = np.array([
    gPump,
    gNav17,
    gNav18,
    gNav19,
    gKs,
    gKf,
    gH,
    gKdr,
    gKna
])

protocol = 42
# -0.5 breaks down the transmission of spikes. Might need to increase to finer ones. Also faster is probably higher conductance, intuitively?? But for all channels?
changes = [-0.2, -0.18, -0.15, -0.1, -0.05, -0.03, 0.0, 0.03, 0.05, 0.1, 0.15, 0.18, 0.2, 0.25]
i_normal = 6
param_names = ['gPump', 'gNav17', 'gNav18', 'gNav19', 'gKs', 'gKf', 'gH', 'gKdr', 'gKna']
params = {}
spikes = {}
for name in param_names:
    params[name] = {}
    spikes[name] = {}
for i, x in enumerate(param_orig):
    for dg in changes:
        param_new = param_orig.copy()
        param_new[i] = param_orig[i] * (1 + dg) # scale 1 parameter

        params[param_names[i]][dg] = param_new

for name in param_names:
    for j, dg in enumerate(changes):
        param = params[name][dg]
        spike = getData(prot=protocol, filetype="spikes", scalingFactor=0.1, gPump=param[0], gNav17=param[1], gNav18=param[2], gNav19=param[3], gKs=param[4], gKf=param[5], gH=param[6], gKdr=param[7], gKna=param[8])
        spikes[name][dg] = spike

data_stim = getData(prot=protocol, filetype="stim")

def get_metrics(data_aps, data_stim, Slow025HzStart=1, Slow025HzEnd=90, Fast2HzStart=90, Fast2HzEnd=450, Fast2HzPost30S=458):
    initial_velocity = calculateVelocity(data_aps, data_stim)[0]
    latency = calculateLatency(spikes[name][dg], data_stim, norm=False)
    latency_points = [latency[Slow025HzStart], latency[Fast2HzStart], latency[Fast2HzEnd], latency[Fast2HzPost30S]]
    Slow025StartToEnd = (latency[Slow025HzEnd] - latency[Slow025HzStart]) / latency[Slow025HzStart]
    Slow025EndToFast2HzEnd = (latency[Fast2HzEnd] - latency[Slow025HzEnd]) / latency[Slow025HzEnd]
    # recovery at 30 s (latency at 30 s after 2 Hz stimulation compared to latency before 0.25 Hz stimulation)
    # can be also negative (but unlikely)
    Fast2HzStartToPost30S = (latency[Fast2HzPost30S] - latency[Slow025HzStart]) / latency[Slow025HzStart]
    TimeTo50Percent = 0 # not implemented yet because it is barely changed by the conductancies
    return (initial_velocity, Slow025StartToEnd, Slow025EndToFast2HzEnd, Fast2HzStartToPost30S, TimeTo50Percent, latency_points)
Slow025HzStart = 1
Slow025HzEnd = 90
Fast2HzStart = 90 # 90 stimulations at 0.25 Hz initially
Fast2HzEnd = 450 # 360 stimulations at 2 Hz
Fast2HzPost30S = Fast2HzEnd + 8 # 32 s after reducing the stimulation frequency from 2 Hz to 0.25 Hz again

points = [Slow025HzStart, Slow025HzEnd, Fast2HzStart, Fast2HzEnd, Fast2HzPost30S, 0]
points_name = ["InitialVelocity", "Slow025HzStart", "Slow025HzEnd", "Fast2HzStart", "Fast2HzEnd", "Fast2HzPost30S", "SimulationEnd"]
slowing_name = [points_name[0], points_name[1]+"-"+points_name[2], points_name[3]+"-"+points_name[4], points_name[5], "TimeTo50Percent"]


# Ribeiro et al: Peripheral C fibers in long COVID, page 9, mean values of Type 1B fibres for COVID and healthy patients
# does the data match?
experiment_values = {}
experiment_values_labels = ["CV", "0to025", "025to2", "30sRecovery", "50%RecoveryTime"]
experiment_values_covid = np.array([0.52, 5.52, 31.8, 31.6, 62.2])
experiment_values_healthy = np.array([0.43, 4.09, 36, 19.7, 96.2])
experiment_factors = experiment_values_covid/experiment_values_healthy

for l, c, h, f in zip(experiment_values_labels, experiment_values_covid, experiment_values_healthy, experiment_factors):
    experiment_values[l] = {}
    experiment_values[l]["Covid"] = c
    experiment_values[l]["Healthy"] = h
    experiment_values[l]["Factor"] = f
#%%
# Optimisation task: Find param that slowing_rel \approx experiment_factors
# We can treat experiment_factors as the product of slowing_rel
# 8 channels, 4 values -> should be possible
# underconstrained problem -> multiple solutions
# LLM says: add regularization constraints (e.g. least deviation from original parameters)
#%%
metric_healthy = np.array(get_metrics(spikes[param_names[0]][changes[i_normal]], data_stim)[0:-1])
experiment_factors[-1] = 0 # time to 50% recovery ignored for now

param_min_0 = param_orig * 0.75
param_max_0 = param_orig * 1.25

param_min = np.minimum(param_min_0, param_max_0)
param_max = np.maximum(param_min_0, param_max_0)


def worker_init_neuron():
    import neuron as neuron
    import os
    neuron.load_mechanisms('./MOD_Tigerholm')



# define range as -25% to +50/+25% of the original parameters as param_orig
def calculate_residual(param, factor_compare=experiment_factors, worker_id=0):
    parameter_sa_run = {
                    'prot': 42,
                    'sine': False,
                    'scalingFactor': 0.1,
                    'gPump': param[0],
                    'gNav17': param[1],
                    'gNav18': param[2],
                    'gNav19': param[3],
                    'gKs': param[4],
                    'gKf': param[5],
                    'gH': param[6],
                    'gKdr': param[7],
                    'gKna': param[8],
                    'vRest': vRest,
                    'log_potential': False,
                    'path': f"temp_{worker_id}/"
                }
    parameter_file = parameter_sa_run.copy()
    parameter_file["filetype"] = "spikes"
    parameter_file.pop("log_potential")
    os.makedirs(parameter_sa_run["path"], exist_ok=True)

    run(**parameter_sa_run) # takes the most time, by far

    spikes_test = getData(**parameter_file )

    metric_test = np.array(get_metrics(spikes_test, data_stim)[0:-1])
    factor_metric = metric_test/metric_healthy

    residual = np.linalg.norm(factor_metric - factor_compare, ord=2)

    return residual

space = [Real(lo, hi, name=n) for n, lo, hi in zip(param_names, param_min, param_max)]
opt = Optimizer(space, base_estimator='GP', acq_func='EI',
                  n_initial_points=10, random_state=42)
n_parallel = 2
n_rounds   = 2

for round_i in range(n_rounds):
    # ask for n_parallel suggestions at once
    xs = opt.ask(n_points=n_parallel)

    # evaluate in parallel — each call runs a separate NEURON sim
    costs = Parallel(n_jobs=n_parallel, initializer=worker_init_neuron)(
        delayed(calculate_residual)(x, worker_id=i) for i, x in enumerate(xs)
    )

    opt.tell(xs, costs)
    print(f"Round {round_i+1:02d} | best so far: {min(opt.yi):.6f}")

x_opt = opt.Xi[np.argmin(opt.yi)]
print(dict(zip(param_names, x_opt)))
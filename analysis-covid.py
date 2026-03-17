import neuron as neuron

from dataProcessing import getData, getFilename, calculateLatency, calculateVelocity
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from stimulationProtocols import getCOVIDFullTime
from plot import plotLatency, plotRecoveryCycle
import os
from main_CMi import run


neuron.load_mechanisms('./MOD_Tigerholm')
#%%
params_orig = {
    'gPump': -0.00485891709589456,
    'gNav17Parent': 0.22831806252579703,
    'gNav17': 0.33198932295899997,
    'gNav18Parent': 0.2411879110860178,
    'gNav18': 0.04520936848183172,
    'gNav19': 0.0032208034421239012,
    'gKs': 0.0030962055552702606,
    'gKf': 0.025994684685553986,
    'gH': 0.009167424690232623,
    'gKdr': 0.013875365047132446,
    'gKna': 0.0014444412024341238,
    'vRest': -55.0
}

changes = [-0.6, -0.4, -0.2, -0.1, 0.1, 0.2, 0.4, 0.6, 0.8]

changes_v_rest = [-0.3, -0.2, -0.1, 0.1, 0.2, 0.4]

changes_gNav18 = [-0.6, -0.4, -0.2, -0.1, 0.1, 0.2, 0.3]

params_dict = {}
filenames = {}
spikes = {}

# assign parameter sets
for name, val in params_orig.items():
    if name in ['gNav17Parent', 'gNav18Parent', 'gKf']:
        continue

    spikes[name] = {}
    params_dict[name] = {}
    filenames[name] = {}
    if name in ['gNav17', 'gNav18']:
        parent_name = name + 'Parent'
        if name == 'gNav18':
            for dg in changes_gNav18:
                new_p = params_orig.copy()
                new_p[name] = params_orig[name] * (1 + dg)
                new_p[parent_name] = params_orig[parent_name] * (1 + dg)
                params_dict[name][dg] = new_p

        else:
            for dg in changes:
                new_p = params_orig.copy()
                new_p[name] = params_orig[name] * (1 + dg)
                new_p[parent_name] = params_orig[parent_name] * (1 + dg)
                params_dict[name][dg] = new_p

    elif name == 'vRest':
        for dg in changes_v_rest:
            new_p = params_orig.copy()
            new_p[name] = params_orig[name] * (1 + dg)
            params_dict[name][dg] = new_p

    else:
        for dg in changes:
            new_p = params_orig.copy()
            new_p[name] = params_orig[name] * (1 + dg)
            params_dict[name][dg] = new_p

i_normal = 6  # where changes = 0
param_names = ['gPump', 'gNav17Parent', 'gNav18Parent', 'gNav19', 'gKs', 'gKf', 'gH', 'gKdr', 'gKna']

fiber_type = 'CMi'

protocol = 42
#%%
for name, dg_dict in params_dict.items():
    for dg, param_dict in dg_dict.items():
        # param_dict contains the properly scaled values for this iteration
        spike = getData(
            prot=protocol,
            filetype="spikes",
            scalingFactor=0.1,
            gPump=param_dict['gPump'],
            gNav17=param_dict['gNav17'],
            gNav17Parent=param_dict['gNav17Parent'],
            gNav18=param_dict['gNav18'],  # this is very confusing because I messed up the naming in run.py
            gNav18Parent=param_dict['gNav18Parent'],
            gNav19=param_dict['gNav19'],
            gKs=param_dict['gKs'],
            gKf=param_dict['gKf'],
            gH=param_dict['gH'],
            gKdr=param_dict['gKdr'],
            gKna=param_dict['gKna'],
            vRest=param_dict['vRest']
        )
        filenames[name][dg] = getFilename(
            prot=protocol,
            filetype="spikes",
            scalingFactor=0.1,
            gPump=param_dict['gPump'],
            gNav17=param_dict['gNav17Parent'],
            gNav17Parent=param_dict['gNav17'],
            gNav18=param_dict['gNav18Parent'],  # this is very confusing because I messed up the naming in run.py
            gNav18Parent=param_dict['gNav18'],
            gNav19=param_dict['gNav19'],
            gKs=param_dict['gKs'],
            gKf=param_dict['gKf'],
            gH=param_dict['gH'],
            gKdr=param_dict['gKdr'],
            gKna=param_dict['gKna'],
            vRest=param_dict['vRest']
        )
        spikes[name][dg] = spike

#%%
data_stim = getData(prot=protocol, filetype="stim")
#plotRecoveryCycle(spikes, data_stim)
print(len(spikes), len(data_stim))
#%%
# add: ignore NAN/iunf?
latencies = np.zeros((len(params_orig), len(changes), len(data_stim)))
latencies_percent = np.zeros((len(params_orig), len(changes), len(data_stim)))
for i, (name, dg_dict) in enumerate(params_dict.items()):
    for j, (dg, param_dict) in enumerate(dg_dict.items()):
        latencies[i][j] = calculateLatency(spikes[name][dg], data_stim, norm=False)[:, 1]  # ms and not ADS %
        latencies_percent[i][j] = calculateLatency(spikes[name][dg], data_stim, norm=True)[:, 1]  # ADS % and not ms
initial_velocities = np.zeros((len(params_orig), len(changes)))
for i, (name, dg_dict) in enumerate(params_dict.items()):
    for j, (dg, param_dict) in enumerate(dg_dict.items()):
        v = calculateVelocity(spikes[name][dg], data_stim)
        initial_velocities[i][j] = v[1]
        if initial_velocities[i][j] == 0.:
            initial_velocities[i][j] = np.nan

#%%
def get_metrics(data_aps, data_stim, Slow025HzStart=1, Slow025HzEnd=90, Fast2HzStart=90, Fast2HzEnd=450,
                Fast2HzPost30S=458):
    initial_velocity = calculateVelocity(data_aps, data_stim)[0]
    latency = calculateLatency(data_aps, data_stim, norm=False)[:, 1]
    latency_points = [latency[Slow025HzStart], latency[Fast2HzStart], latency[Fast2HzEnd], latency[Fast2HzPost30S]]
    Slow025StartToEnd = (latency[Slow025HzEnd] - latency[Slow025HzStart]) / latency[Slow025HzStart]
    Slow025EndToFast2HzEnd = (latency[Fast2HzEnd] - latency[Slow025HzEnd]) / latency[Slow025HzEnd]
    # recovery at 30 s (latency at 30 s after 2 Hz stimulation compared to latency before 0.25 Hz stimulation)
    # can be also negative (but unlikely)
    Fast2HzStartToPost30S = (latency[Fast2HzPost30S] - latency[Slow025HzStart]) / latency[Slow025HzStart]
    TimeTo50Percent = 0  # not implemented yet because it is barely changed by the conductancies
    return (initial_velocity, Slow025StartToEnd, Slow025EndToFast2HzEnd, Fast2HzStartToPost30S, TimeTo50Percent,
            latency_points)

#%%
Slow025HzStart = 1
Slow025HzEnd = 90
Fast2HzStart = 90  # 90 stimulations at 0.25 Hz initially
Fast2HzEnd = 450  # 360 stimulations at 2 Hz
Fast2HzPost30S = Fast2HzEnd + 8  # 32 s after reducing the stimulation frequency from 2 Hz to 0.25 Hz again
# last one is the end of simulation
SimulationEnd = latencies.shape[2] - 1
points = [Slow025HzStart, Slow025HzEnd, Fast2HzStart, Fast2HzEnd, Fast2HzPost30S, SimulationEnd]
points_name = ["InitialVelocity", "Slow025HzStart", "Slow025HzEnd", "Fast2HzStart", "Fast2HzEnd", "Fast2HzPost30S",
               "SimulationEnd"]
slowing_name = [points_name[0], points_name[1] + "-" + points_name[2], points_name[3] + "-" + points_name[4],
                points_name[5], "TimeTo50Percent"]

latencies_at_points = np.zeros((len(params_orig), len(changes), 6))  # at special points
slowing_abs = np.zeros(
    (len(params_orig), len(changes), 5))  # Slowing 0 to 0.25, 0.25 to 2, recovery at 30 s, Time to 50% recovery
#%%
# as dicts
latency_dict = {}
slowing_dict = {}

for i, (name, dg_dict) in enumerate(params_dict.items()):
    latency_dict[name] = {}
    slowing_dict[name] = {}
    for j, (dg, param_dict) in enumerate(dg_dict.items()):
        latency_dict[name][dg] = {}
        slowing_dict[name][dg] = {}
        for k, (point, point_name) in enumerate(zip(points, points_name)):
            latencies_at_points[i][j][k] = latencies[i][j][point]
            latency_dict[name][dg][point_name] = latencies[i][j][point]

        metric = get_metrics(spikes[name][dg], data_stim)
        # Initial velocity
        slowing_abs[i][j][0:4] = metric[0:4]
        slowing_dict[name][dg][slowing_name[0]] = slowing_abs[i][j][0]
        slowing_dict[name][dg][slowing_name[1]] = slowing_abs[i][j][1]
        slowing_dict[name][dg][slowing_name[2]] = slowing_abs[i][j][2]
        slowing_dict[name][dg][slowing_name[3]] = slowing_abs[i][j][3]

        recovery_50_percent_threshold = (latencies[i][j][Fast2HzStart] + latencies[i][j][Fast2HzEnd]) / 2
        # time to 50 % recovery
        for n in np.arange(Fast2HzEnd, SimulationEnd):
            # if the latency at number t-th spike is lower than the 50 % recovery threshold
            if latencies[i][j][n] < recovery_50_percent_threshold:
                # use the time as the time until 50 % recovery
                slowing_abs[i][j][4] = getCOVIDFullTime(n) - getCOVIDFullTime(
                    Fast2HzStart)  # can be made more precise with linear interpolation
                slowing_dict[name][dg][slowing_name[4]] = slowing_abs[i][j][4]
                break

        slowing_abs[np.where(slowing_abs == 0.)] = np.nan

#%%
getCOVIDFullTime(90)
#%%
# Plot raw latencies
fig, axes = plt.subplots(len(param_names), 1, figsize=(6, 6*len(param_names)))
for i, name_g in enumerate(param_names):
    ax = axes[i]
    latency = latencies[i]
    for j, latency in enumerate(latency):
        ax.plot(latency, alpha=0.8, label=f"{name_g} {changes[j]*100:.2f}%")

    ax.set_xlabel("Action potential")
    ax.set_ylabel("Latency [ms] ")
    ax.legend()
    ax.grid(True)
    ax.set_title(f"Latency when varying {name_g}")
plt.savefig(f"Results/raw_latency_plot_{fiber_type}.pdf")
#%%
# Plot relative latencies
fig, axes = plt.subplots(len(param_names), 1, figsize=(6, 6*len(param_names)))
for i, name_g in enumerate(param_names):
    ax = axes[i]
    latency = latencies_percent[i]
    for j, latency in enumerate(latency):
        ax.plot(latency, alpha=0.8, label=f"{name_g} {changes[j]*100:.2f}%")

    ax.set_xlabel("Action potential")
    ax.set_ylabel("Latency (%)")
    ax.legend()
    ax.grid(True)
    ax.set_title(f"Latency when varying {name_g}")
plt.savefig(f"Results/raw_ADS_plot_{fiber_type}.pdf")
#%%
# Plot slowings
fig, axes = plt.subplots(len(param_names), slowing_abs.shape[-1], figsize=(35, 5*len(param_names)))
# Different parameters
for i, name_g in enumerate(param_names):
    slowings = slowing_abs[i]
    # Different changes
    for j in np.arange(slowings.shape[1]):
        axes[i,j].plot(changes, slowings[:, j], alpha=0.8, label=f"{name_g} ")
        #axes[i,j].set_xticks(changes[::3])
        axes[i,j].set_xlabel(f"Change {name_g}")
        axes[i,0].set_ylabel("Velocity [mm/ms]") # IS THIS UNIT MM/MS CORRECT?? see unit of calculateVelocity
        for k in (1, 2, 3):
            axes[i,k].set_ylabel("Change in latency [%]")
        axes[i,4].set_ylabel("Time to 50% recovery [us]")
        axes[i,j].grid(True)
        axes[i,j].legend()
        axes[i, j].set_title(f"{slowing_name[j]}")
plt.savefig(f"Results/relative_slowings_plot_{fiber_type}.pdf")
#%%
# Plot deviations to "normal" model

# Normalize slowings to slowing with zero changes to original parameters
normal_value = slowing_abs[:, i_normal, :]
slowing_rel = slowing_abs / normal_value[:, np.newaxis, :] # divide/normalize by respective value of original parameter that was not changed

# Plot slowings
fig, axes = plt.subplots(len(param_names), slowing_rel.shape[-1], figsize=(35, 5*len(param_names)))
# Different parameters
for i, name_g in enumerate(param_names):
    slowings_norm = slowing_rel[i]

    # Different changes
    for j in np.arange(slowings_norm.shape[1]):
        axes[i,j].plot(changes, slowings_norm[:, j], alpha=0.8, label=f"{name_g} ")
        #axes[i,j].set_xticks(changes[::3])
        axes[i,j].set_xlabel(f"Change {name_g}")
        axes[i,0].set_ylabel("Relative change in velocity")
        for k in (1, 2, 3):
            axes[i,k].set_ylabel("Relative change in latency")
        axes[i,4].set_ylabel("Relative Time to 50% recovery")
        axes[i,j].grid(True)
        axes[i,j].legend()
        axes[i, j].set_title(f"{slowing_name[j]}")

plt.suptitle(f"Changes, relative to original model")
plt.savefig(f"Results/relative_slowings_normalized_plot_{fiber_type}.pdf")

#%%
# Ribeiro et al: Peripheral C fibers in long COVID, page 9, mean values of Type 1B fibres for COVID and healthy patients
# Data does not match!
experiment_values = {}
experiment_values_labels = ["CV", "0to025", "025to2", "30sRecovery", "50%RecoveryTime"]
experiment_values_covid = np.array([0.52, 5.52, 31.8, 31.6, 62.2])
experiment_values_healthy = np.array([0.43, 4.09, 36, 19.7, 96.2])
experiment_factors = experiment_values_covid/experiment_values_healthy

metric_compare_group = np.array(get_metrics(spikes[param_names[0]][changes[i_normal]], data_stim)[0:-1])

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
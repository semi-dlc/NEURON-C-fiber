import neuron as neuron

from dataProcessing import getData, getFilename, calculateLatency, calculateVelocity
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from stimulationProtocols import getCOVIDFullTime
from plot import plotLatency, plotRecoveryCycle
import os
from main_CM import run

neuron.load_mechanisms('./MOD_Tigerholm')
#%%

params_orig = {
    'gPump': -0.0025,
    'gNav17Parent': 0.13115152763095123,
    'gNav17': 0.24686453257354574,
    'gNav18Parent': 0.23439203005798895,
    'gNav18': 0.37673567973121774,
    'gNav19': 0.00017254238997420438,
    'gKs': 0.008865226128662577,
    'gKf': 0.02709394494148292,
    'gH': 0.014140202887083592,
    'gKdr': 0.008469950837206652,
    'gKna': 0.001398204170298818,
    'vRest': -55
}

changes = [-0.6, -0.4, -0.2, -0.1, 0.1, 0.2, 0.4, 0.6, 0.8]
changes_v_rest = [-0.3, -0.2, -0.1, 0.1, 0.2, 0.4]
changes_gNav18 = [-0.6, -0.4, -0.2, -0.1, 0.1, 0.2, 0.3]
#%%

params_dict = {}
filenames = {}
spikes = {}

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

i_normal = 3 # should include 0 later
param_names = ['gPump', 'gNav17Parent', 'gNav18Parent', 'gNav19', 'gKs', 'gKf', 'gH', 'gKdr', 'gKna']

fiber_type = 'CM'
protocol = 42
#%%
for name, dg_dict in params_dict.items():
    for dg, param_dict in dg_dict.items():
        spike = getData(
            prot=protocol,
            filetype="spikes",
            scalingFactor=0.1,
            gPump=param_dict['gPump'],
            gNav17=param_dict['gNav17Parent'],# due to human error in run.py
            gNav17Parent=param_dict['gNav17'],
            gNav18=param_dict['gNav18Parent'],  # due to human error in run.py
            gNav18Parent=param_dict['gNav18'],
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
            gNav17=param_dict['gNav17Parent'],# due to human error in run.py
            gNav17Parent=param_dict['gNav17'],
            gNav18=param_dict['gNav18Parent'],  # due to human error in run.py
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

data_stim = getData(prot=protocol, filetype="stim")
print(len(spikes), len(data_stim))

latencies = {}
latencies_percent = {}
for name, dg_dict in params_dict.items():
    latencies[name] = {}
    latencies_percent[name] = {}
    for dg in dg_dict:
        latencies[name][dg] = calculateLatency(spikes[name][dg], data_stim, norm=False)[:, 1]
        latencies_percent[name][dg] = calculateLatency(spikes[name][dg], data_stim, norm=True)[:, 1]

initial_velocities = {}
for name, dg_dict in params_dict.items():
    initial_velocities[name] = {}
    for dg in dg_dict:
        initial_velocities[name][dg] = calculateVelocity(spikes[name][dg], data_stim)[1]

#%%

def get_metrics(data_aps, data_stim, Slow025HzStart=1, Slow025HzEnd=90, Fast2HzStart=90, Fast2HzEnd=450,
                Fast2HzPost30S=458):
    initial_velocity = calculateVelocity(data_aps, data_stim)[0]
    latency = calculateLatency(data_aps, data_stim, norm=False)[:, 1]
    latency_points = [latency[Slow025HzStart], latency[Fast2HzStart], latency[Fast2HzEnd], latency[Fast2HzPost30S]]
    Slow025StartToEnd = (latency[Slow025HzEnd] - latency[Slow025HzStart]) / latency[Slow025HzStart]
    Slow025EndToFast2HzEnd = (latency[Fast2HzEnd] - latency[Slow025HzEnd]) / latency[Slow025HzEnd]
    Fast2HzStartToPost30S = (latency[Fast2HzPost30S] - latency[Slow025HzStart]) / latency[Slow025HzStart]
    TimeTo50Percent = 0
    return (initial_velocity, Slow025StartToEnd, Slow025EndToFast2HzEnd, Fast2HzStartToPost30S, TimeTo50Percent,
            latency_points)

#%%

Slow025HzStart = 1
Slow025HzEnd = 90
Fast2HzStart = 90
Fast2HzEnd = 450
Fast2HzPost30S = Fast2HzEnd + 8

_ref_name = next(iter(latencies))
_ref_dg = next(iter(latencies[_ref_name]))
SimulationEnd = len(latencies[_ref_name][_ref_dg]) - 1

points = [Slow025HzStart, Slow025HzEnd, Fast2HzStart, Fast2HzEnd, Fast2HzPost30S, SimulationEnd]
points_name = ["InitialVelocity", "Slow025HzStart", "Slow025HzEnd", "Fast2HzStart",
               "Fast2HzEnd", "Fast2HzPost30S", "SimulationEnd"]
slowing_name = [points_name[0],
                points_name[1] + "-" + points_name[2],
                points_name[3] + "-" + points_name[4],
                points_name[5],
                "TimeTo50Percent"]

latency_dict = {}
slowing_dict = {}
#%%

for name, dg_dict in params_dict.items():
    latency_dict[name] = {}
    slowing_dict[name] = {}
    for dg in dg_dict:
        latency_dict[name][dg] = {}
        slowing_dict[name][dg] = {}

        for point, point_name in zip(points, points_name):
            latency_dict[name][dg][point_name] = latencies[name][dg][point]

        metric = get_metrics(spikes[name][dg], data_stim)
        slowing_dict[name][dg][slowing_name[0]] = metric[0]
        slowing_dict[name][dg][slowing_name[1]] = metric[1]
        slowing_dict[name][dg][slowing_name[2]] = metric[2]
        slowing_dict[name][dg][slowing_name[3]] = metric[3]

        slowing_dict[name][dg][slowing_name[4]] = np.nan  # overwritten if threshold is crossed
        recovery_50_threshold = (latencies[name][dg][Fast2HzStart] + latencies[name][dg][Fast2HzEnd]) / 2
        for n in np.arange(Fast2HzEnd, SimulationEnd):
            if latencies[name][dg][n] < recovery_50_threshold:
                slowing_dict[name][dg][slowing_name[4]] = getCOVIDFullTime(n) - getCOVIDFullTime(Fast2HzStart)
                break

getCOVIDFullTime(90)
#%%
fig, axes = plt.subplots(len(params_dict), 1, figsize=(6, 6 * len(params_dict)))
for ax, (name, dg_dict) in zip(axes, params_dict.items()):
    for dg, lat in latencies[name].items():
        ax.plot(lat, alpha=0.8, label=f"{name} {dg * 100:.2f}%")
    ax.set_xlabel("Action potential")
    ax.set_ylabel("Latency [ms]")
    ax.legend()
    ax.grid(True)
    ax.set_title(f"Latency when varying {name}")
plt.savefig(f"Results/raw_latency_plot_{fiber_type}.pdf")
#%%

fig, axes = plt.subplots(len(params_dict), 1, figsize=(6, 6 * len(params_dict)))
for ax, (name, dg_dict) in zip(axes, params_dict.items()):
    for dg, lat in latencies_percent[name].items():
        ax.plot(lat, alpha=0.8, label=f"{name} {dg * 100:.2f}%")
    ax.set_xlabel("Action potential")
    ax.set_ylabel("Latency (%)")
    ax.legend()
    ax.grid(True)
    ax.set_title(f"Latency when varying {name}")
plt.savefig(f"Results/raw_ADS_plot_{fiber_type}.pdf")
#%%
fig, axes = plt.subplots(len(params_dict), len(slowing_name), figsize=(35, 5 * len(params_dict)))
for i, (name, dg_dict) in enumerate(params_dict.items()):
    dg_list = list(dg_dict.keys())
    for j, sname in enumerate(slowing_name):
        values = [slowing_dict[name][dg].get(sname, np.nan) for dg in dg_list]
        axes[i, j].plot(dg_list, values, alpha=0.8, label=name)
        axes[i, j].set_xlabel(f"Change {name}")
        axes[i, 0].set_ylabel("Velocity [mm/ms]")
        for k in (1, 2, 3):
            axes[i, k].set_ylabel("Change in latency [%]")
        axes[i, 4].set_ylabel("Time to 50% recovery [us]")
        axes[i, j].grid(True)
        axes[i, j].legend()
        axes[i, j].set_title(sname)
plt.savefig(f"Results/relative_slowings_plot_{fiber_type}.pdf")
#%%
# For each parameter, normalize each metric by its value at the reference dg.
# Reference dg: changes[i_normal] if available (params using `changes`),
# otherwise the first available dg (vRest uses changes_v_rest, gNav18 uses changes_gNav18).
fig, axes = plt.subplots(len(params_dict), len(slowing_name), figsize=(35, 5 * len(params_dict)))
for i, (name, dg_dict) in enumerate(params_dict.items()):
    dg_list = list(dg_dict.keys())
    ref_dg = changes[i_normal] if changes[i_normal] in dg_dict else dg_list[0]
    for j, sname in enumerate(slowing_name):
        ref_val = slowing_dict[name][ref_dg].get(sname, np.nan)
        values = [slowing_dict[name][dg].get(sname, np.nan) / ref_val for dg in dg_list]
        axes[i, j].plot(dg_list, values, alpha=0.8, label=name)
        axes[i, j].set_xlabel(f"Change {name}")
        axes[i, 0].set_ylabel("Relative change in velocity")
        for k in (1, 2, 3):
            axes[i, k].set_ylabel("Relative change in latency")
        axes[i, 4].set_ylabel("Relative time to 50% recovery")
        axes[i, j].grid(True)
        axes[i, j].legend()
        axes[i, j].set_title(sname)
plt.suptitle("Changes, relative to original model")
plt.savefig(f"Results/relative_slowings_normalized_plot_{fiber_type}.pdf")
#%%
# Ribeiro et al: Peripheral C fibers in long COVID, page 9, mean values of Type 1B fibres
experiment_values = {}
experiment_values_labels = ["CV", "0to025", "025to2", "30sRecovery", "50%RecoveryTime"]
experiment_values_covid = np.array([0.52, 5.52, 31.8, 31.6, 62.2])
experiment_values_healthy = np.array([0.43, 4.09, 36, 19.7, 96.2])
experiment_factors = experiment_values_covid / experiment_values_healthy

ref_name = param_names[0]  # 'gPump'
ref_dg = changes[i_normal]  # 0.4
metric_compare_group = np.array(get_metrics(spikes[ref_name][ref_dg], data_stim)[0:-1])

for l, c, h, f in zip(experiment_values_labels, experiment_values_covid,
                      experiment_values_healthy, experiment_factors):
    experiment_values[l] = {"Covid": c, "Healthy": h, "Factor": f}

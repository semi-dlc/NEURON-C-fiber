import neuron as neuron
import main_CM
from multiprocessing import Pool

neuron.load_mechanisms('./MOD_Tigerholm')

params = []

gPump = -0.0025
gNav17 = 0.24686453257354574
gNav17Parent=0.13115152763095123
gNav18 = 0.37673567973121774
gNav18Parent=0.23439203005798895
gNav19 = 0.00017254238997420438
gKs = 0.008865226128662577
gKf = 0.02709394494148292
gH = 0.014140202887083592
gKdr = 0.008469950837206652
gKna = 0.001398204170298818
vRest = -55

param_orig = [
    gPump,
    gNav17Parent,
    gNav18Parent,
    gNav19,
    gKs,
    gKf,
    gH,
    gKdr,
    gKna
]

param_names = ['gPump', 'gNav17Parent', 'gNav18Parent', 'gNav19', 'gKs', 'gKf', 'gH', 'gKdr', 'gKna']

changes = [-0.2, -0.15, -0.1, -0.05, 0.0, 0.05, 0.1, 0.15, 0.2, 0.25]

for dg in changes:
    for i, x in enumerate(param_orig):
        param_new = param_orig.copy()
        param_new[i] = param_orig[i] * (1 + dg) # scale 1 parameter
        params.append(param_new)

if __name__ == '__main__':
    # Parallelize the execution
    with Pool(processes=5) as pool:
        results = []
        for param in params:
            # Create kwargs dictionary with varied parameters
            kwargs = {
                'prot': 42,
                'sine': False,
                'scalingFactor': 0.1,
                'gPump': param[0],
                'gNav17Parent': param[1],
                'gNav18Parent': param[2],
                'gNav19': param[3],
                'gKs': param[4],
                'gKf': param[5],
                'gH': param[6],
                'gKdr': param[7],
                'gKna': param[8],
                'vRest': vRest
            }

            # Submit job to pool with keyword arguments
            result = pool.apply_async(main_CM.run, kwds=kwargs)
            results.append(result)

        # Wait for all results to complete
        output = [r.get() for r in results]
import neuron as neuron
import main_CMi
from multiprocessing import Pool

neuron.load_mechanisms('./MOD_Tigerholm')

params = []

gPump = -0.00485891709589456
gNav17 = 0.33198932295899997
gNav17Parent=0.22831806252579703
gNav18 = 0.04520936848183172
gNav18Parent=0.2411879110860178
gNav19 = 0.0032208034421239012
gKs = 0.0030962055552702606
gKf = 0.025994684685553986
gH = 0.009167424690232623
gKdr = 0.013875365047132446
gKna = 0.0014444412024341238
vRest = -55

param_orig = [
    gPump,
    gNav17,
    gNav18,
    gNav19,
    gKs,
    gKf,
    gH,
    gKdr,
    gKna
]

param_names = ['gPump', 'gNav17', 'gNav18', 'gNav19', 'gKs', 'gKf', 'gH', 'gKdr', 'gKna']

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
                'gNav17': param[1],
                'gNav18': param[2],
                'gNav19': param[3],
                'gKs': param[4],
                'gKf': param[5],
                'gH': param[6],
                'gKdr': param[7],
                'gKna': param[8],
                'vRest': vRest
            }

            # Submit job to pool with keyword arguments
            result = pool.apply_async(main.run, kwds=kwargs)
            results.append(result)

        # Wait for all results to complete
        output = [r.get() for r in results]
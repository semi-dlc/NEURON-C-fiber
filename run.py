import neuron as neuron
import main

neuron.load_mechanisms('./MOD_Tigerholm')
main.run(prot=40, sine=False)

main.run(prot=41, sine=False)
# NeuralSim Extended Network with Optogenetic Stimulation
# Created by Cameron Yenche

from neuron import h, gui
import matplotlib.pyplot as plt
import random

# Parameters
NUM_NEURONS = 50  # Total number of neurons
NUM_INPUT_LAYER = 10  # Number of neurons in the input layer

# Create a list to store neurons
neurons = []
for i in range(NUM_NEURONS):
    soma = h.Section(name=f'soma_{i}')
    soma.L = 20
    soma.diam = 20
    soma.insert('hh')
    # Increase sodium conductance and/or decrease potassium conductance for easier spiking
    soma(0.5).hh.gnabar = 0.15  # Increase sodium conductance (default is typically 0.12)
    soma(0.5).hh.gkbar = 0.036  # Decrease potassium conductance (default is typically 0.036)
    if i < NUM_INPUT_LAYER:
        soma.insert('ChR2')  # Add ChR2 mechanism only for input layer neurons
    neurons.append(soma)

# Function to create synaptic connections between neurons
def create_synaptic_connection(pre, post, weight=2.0, delay=2.0):
    syn = h.ExpSyn(post(0.5))
    syn.tau = 2.0
    syn.e = 0  # Synaptic reversal potential
    netcon = h.NetCon(pre(0.5)._ref_v, syn, sec=pre)
    netcon.weight[0] = weight
    netcon.delay = delay
    return netcon

# Create synaptic connections in a feedforward and partially random manner
connections = []
for i in range(NUM_NEURONS - 1):
    # Regular feedforward connection
    connections.append(create_synaptic_connection(neurons[i], neurons[i + 1]))
    # Additional random connections to add variability
    if i + 2 < NUM_NEURONS and random.random() < 0.5:  # 50% chance of extra connection
        connections.append(create_synaptic_connection(neurons[i], neurons[i + 2], weight=1.0))

# Add Stimulus to the first neuron (input layer)
stim = h.IClamp(neurons[0](0.5))  # Stimulate the first neuron
stim.delay = 5.0  # Start time of stimulation (ms)
stim.dur = 1.0    # Duration of stimulation (ms)
stim.amp = 0.2    # Amplitude of stimulation (nA)

# Add Optogenetic Light Input (simulating light activation of opsins) for input layer neurons
light_stims = []
for i in range(NUM_INPUT_LAYER):
    light_stim = h.IClamp(neurons[i](0.5))  # Simulate light input
    light_stim.delay = 10.0  # Start time of light stimulation (ms)
    light_stim.dur = 10.0     # Duration of light exposure (ms)
    light_stim.amp = 1.0     # Light intensity in arbitrary units
    light_stims.append(light_stim)

# Record Data from all neurons
recordings = []
time = h.Vector().record(h._ref_t)  # Record time
for i, soma in enumerate(neurons):
    v = h.Vector().record(soma(0.5)._ref_v)  # Record membrane potential
    recordings.append(v)

# Run the Simulation
h.finitialize(-65)  # Set the initial membrane potential (mV)
h.continuerun(200.0)  # Run the simulation for 100 ms

# Plot Results
plt.figure(figsize=(15, 10))
for i in range(NUM_NEURONS):
    plt.plot(time, recordings[i], label=f'Neuron {i + 1}')
plt.xlabel('Time (ms)')
plt.ylabel('Membrane Potential (mV)')
plt.title('Network with Optogenetic Stimulation in Input Layer')
plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1))
plt.show()

# Print final voltage of each neuron to check which neurons are depolarized or spiking
for i, soma in enumerate(neurons):
    print(f"Neuron {i} final voltage: {recordings[i][-1]} mV")
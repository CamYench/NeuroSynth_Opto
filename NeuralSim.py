# NeuralSim
# 
# Created by Cameron Yenche 11-06-2024
# 
# This is an extension of a basic Neural Network Simulation into a simple network

# Import Modules
from neuron import h, gui
import matplotlib.pyplot as plt


# Define Simple Neuron Cell (soma 1)
soma1 = h.Section(name='soma1')  # Create a soma section
soma1.L = 20                    # Length of the soma
soma1.diam = 20                 # Diameter of the soma
soma1.insert('hh')              # Insert Hodgkin-Huxley dynamics (Na+ and K+ channels)

# Create the second cell (soma2)
soma2 = h.Section(name='soma2')
soma2.L = 20
soma2.diam = 20
soma2.insert('hh')  # Insert Hodgkin-Huxley dynamics

# Create a Synapse between soma 1 and soma 2
syn = h.ExpSyn(soma2(0.5))  # Exponential synapse at soma2
syn.tau = 2.0               # Time constant of synaptic conductance (ms)
syn.e = 0                   # Reversal potential (mV)

# Connect the neurons using a NetCon object
netcon = h.NetCon(soma1(0.5)._ref_v, syn, sec=soma1)
netcon.weight[0] = 0.1     # Synaptic weight
netcon.delay = 5.0         # Transmission delay (ms)


# Add Stimulus (current clamp)
stim = h.IClamp(soma1(0.5))  # Attach current clamp to the middle of the soma
stim.delay = 5.0            # Start of stimulation (ms)
stim.dur = 1.0              # Duration of stimulation (ms)
stim.amp = 0.1              # Amplitude of stimulation (nA)

# Set up recording vectors for both neurons
v1 = h.Vector().record(soma1(0.5)._ref_v)  # Record membrane potential of soma1
v2 = h.Vector().record(soma2(0.5)._ref_v)  # Record membrane potential of soma2
t = h.Vector().record(h._ref_t)            # Record time

# Run the Simulation
h.finitialize(-65)  # Set the initial membrane potential (mV)
h.continuerun(40.0) # Run the simulation for 40 ms

# Plot Results
plt.figure(figsize=(10, 4))
plt.plot(t, v1, label='Neuron 1 (soma1)')
plt.plot(t, v2, label='Neuron 2 (soma2)')
plt.xlabel('Time (ms)')
plt.ylabel('Membrane potential (mV)')
plt.title('Simple Two-Neuron Network Simulation')
plt.legend()
plt.show()
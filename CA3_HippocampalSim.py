# NeuralSim CA3 Hippocampal Pyramidal Cell Simulation
# Created by Cameron Yenche

'''
The CA3 pyramidal cell is modelled as follows:
- Morphological sections (soma and dendrite)
- Biophysical mechanisms (active ion channels and passive properties)
- 3 types of synapses (A/C, PP, and MF) with distinct dynamics
    - Associational / Commissural (A/C) Synapses: formed by the inputs from CA3 pyramidal neurons onto other CA3 pyramidal neurons via local (associational) and contralateral (commissural) projections -- these play a role in recurrent excitatory connectivity, which is associated with memory storage and pattern completion
        - Mediated by AMPA and NMDA receptators
        - Slower kinetics (rise and decay times) when compared to mossy fiber inputs
        - Positioned at 50% of the dendritic length, representing a typical location in the stratum radiatum
    - Perforant Path (PP) Synapses: provide an input from the entorhinal cortex (layer II) to the CA3 region -- these synapses form a critical component of the hippocampal trisynaptic circuit
        - Input source is from axons in the entorhinal cortex via PP
        - Found in the stratum lacunosum-moleculare of the CA3 dendrites
        - Also mediated by AMPA and NMDA
        - Longer rise and decay times when compared to A/C synapses due to distal dendritical location and input dynamics
        - Positioned at 70% of the dendritic length, representing the distal dendritic location
    - Mossy Fiber (MF) Synapses: formed by granule cells in the dentate gyrus projecting onto the CA3 pyramidal neurons; they are large with multiple active zones, which allows for strong and rapid excitatory signaling -- they are crucial for feedforward excitation, driving CA3 activity in response to sensory input
        - Located on the proximal dendrites of CA3 pyramidal cells (near the soma)
        - Mediated by AMPA and NMDA receptors
        - Very fast kinetics due to their role in high-frequency input processing
        - Positioned at 30$ of the dendritic length, representing the proximal dendritic location. 
- Stimulus generators to envoke synaptic responses
'''

from neuron import h, gui
import matplotlib.pyplot as plt

# --- Define Morphology ---
soma = h.Section(name='soma') # Create a compartment named soma to represent the main cell body
soma.L, soma.diam = 20, 20 # Set the length (L) and diameter (diam) of the soma to 20 microns each, this makes it spherical
soma.nseg = 1 # Define the number of segments in the soma (1 is enough since it is spherical)
soma.Ra = 150  # Axial resistivity set to 150 ohm·cm (this affects how current flows within the nueron)
soma.cm = 1.0  # Membrane capacitance (cm) set to 1.0 µF/cm² (this defines the membrane's ability to store charge)

# Add dendrites
dend = h.Section(name='dend') # Create a dendrite section named dend 
dend.L, dend.diam = 200, 2 # Set the dendrite dimensions to have a length of 200 microns and a diameter of 2 microns
dend.nseg = 11 # Divide the dendrite into 11 segments (for more accurate spatial simiulations)
dend.Ra = 150 # Axial resistivity set to 150 ohm·cm
dend.cm = 1.0 # Membrane capacitance (cm) set to 1.0 µF/cm²
dend.connect(soma(1)) # Connects the dendrite to the soma at the distal end; (soma(1)) refers to the far end of the soma

# --- Insert Mechanisms ---
# Somatic mechanisms
soma.insert('hh')  # Insert Hodgkin-Huxley channel dynamics into the soma, modeling sodium (NA⁺) and potassium (K⁺) channels with leak conductance.
soma.insert('Kdr')  # Insert delayed rectifier potassium channels (Kdr) into the soma for repolarization during action potentials
soma.insert('Na')  # Insert Sodium channels to model fast depolarizing currents.

# Dendritic mechanisms (Adds specialized potassium channels to the dendrite to replicate observed properties in CA3 pyramidal cells)
dend.insert('KaProx')  # Proximal A-type potassium channel
dend.insert('KdBG')  # Additional dendritic potassium

# --- Define Synapses ---
# A/C Synapse (associational/commissural pathway)
ac_syn = h.Exp2Syn(dend(0.5)) # Create an Exp2Syn synapse on the dendrite at 50% of it's length; Exp2Syn models double exponential conductance changes (commonly used)
ac_syn.tau1, ac_syn.tau2 = 0.4, 4.1 # Set the synaptic rise time (tau1 = 0.4 ms) and decay time (tau2 = 4.1 ms)
ac_syn.e = 0  # Define the reversal potential as 0 mV (representing excitatory input)

# Perforant Path (PP) Synapse
pp_syn = h.Exp2Syn(dend(0.7)) # Creates a perforant path (PP) synapse at 70% of the dendrite length
pp_syn.tau1, pp_syn.tau2 = 0.5, 5.0 # Add slightly longer time constraints
pp_syn.e = 0  # Set the reversal potential to 0 mV

# Mossy Fiber (MF) Synapse
mf_syn = h.Exp2Syn(dend(0.3)) # Adds a mossy fiber (MF) synapse close to the soma (30% along the dendrite)
mf_syn.tau1, mf_syn.tau2 = 0.3, 1.8 # Adjust for faster dynamics
mf_syn.e = 0 # Set the reversal potential to 0 mV

# --- Create Stimuli ---
stim_ac = h.NetStim() # Create a NetStim object to generate spike trains
stim_ac.number = 5 # Define train of 5 spikes
stim_ac.start = 10 # Start the spike train at 10 ms
stim_ac.interval = 10 # Set the spike train intervals to be 10 ms long

stim_pp = h.NetStim() # Create another NetStim object for the PP synapse
stim_pp.number = 3 # Define a spike train of 3
stim_pp.start = 20 # Start the spike train at 20 ms
stim_pp.interval = 20 # Set the spike train intervals to be 20 ms long

stim_mf = h.NetStim() # Create another NetStim object for the MF synapse
stim_mf.number = 3 # Define spike train of 3
stim_mf.start = 30 # Start the spike train at 30 ms
stim_mf.interval = 15 # Set the spike train intervals to be 15 ms long

# Connect stimuli to synapses
ac_netcon = h.NetCon(stim_ac, ac_syn) # Link the stim_ac generator to the A/C synapse - Associational / Commissural (A/C) Synapses
ac_netcon.weight[0] = 0.01 # Assign a synaptic weight of 0.01 µS

pp_netcon = h.NetCon(stim_pp, pp_syn) # Connects the stim_pp generator to the PP synapse
pp_netcon.weight[0] = 0.01 # Assign a synaptic weight of 0.01 µS

mf_netcon = h.NetCon(stim_mf, mf_syn) # Link the stim_mf generator to the MF synapse
mf_netcon.weight[0] = 0.01 # Assign a synaptic weight of 0.01 µS

# --- Recording ---
t = h.Vector().record(h._ref_t)  # Records time through the simulation
v_soma = h.Vector().record(soma(0.5)._ref_v)  # Records the membrane potential at the midpoint of the Soma [Soma voltage]
v_dend = h.Vector().record(dend(0.5)._ref_v)  # Records the membrane potential at the midpoint of the dendrite [Dendrite voltage]

# --- Simulation ---
h.tstop = 100  # Simulation duration
h.run() # Run the Sim

# --- Plot Results ---
plt.figure(figsize=(10, 6))
plt.plot(t, v_soma, label='Soma Voltage')
plt.plot(t, v_dend, label='Dendrite Voltage', linestyle='--')
plt.xlabel('Time (ms)')
plt.ylabel('Membrane Potential (mV)')
plt.legend()
plt.title('CA3 Pyramidal Cell Synaptic Responses')
plt.show()
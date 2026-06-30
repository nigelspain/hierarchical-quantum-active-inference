import stim
import numpy as np

# We puncture the lattice by defining a circuit with an "open" boundary
# where ancilla 4 is not forced to commute with the data.
circuit = stim.Circuit("""
    R 0 1 2 3
    # Puncture the lattice by leaving Qubit 0 un-stabilized
    # Inject error on the un-stabilized qubit
    X_ERROR(0.5) 0
    
    # Twist: Move the defect by braiding it with qubit 1
    H 0 1
    
    # Destructive readout of the puncture site
    M 0 1
    OBSERVABLE_INCLUDE(0) rec[-1]
""")

sampler = circuit.compile_detector_sampler()
shots = sampler.sample(shots=20, separate_observables=True)
print("--- Topological Charge Manifestation ---")
print(shots[1])

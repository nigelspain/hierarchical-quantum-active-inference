import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.circuit.library import XGate

class SpaceTime4DAggregator:
    def __init__(self, spatial_dim=3):
        self.lattice = np.zeros((spatial_dim, spatial_dim, spatial_dim))
        
    def detect_syndrome(self, injected_qubit_idx):
        # Maps the physical index of the noise to a 3D coordinate
        coord = np.unravel_index(injected_qubit_idx, self.lattice.shape)
        self.lattice[coord] = 1 # Mark defect
        return coord

def run_noise_simulation():
    # 1. Setup
    simulator = AerSimulator()
    qc = QuantumCircuit(3, 3)
    
    # 2. Inject Noise (Bit-Flip on Qubit 1)
    print("--- Injecting Noise: Pauli-X on Qubit 1 ---")
    qc.x(1) 
    
    # 3. Syndrome Extraction (Simplified parity check)
    qc.measure([0, 1, 2], [0, 1, 2])
    
    # 4. Aggregation
    aggregator = SpaceTime4DAggregator()
    syndrome_coord = aggregator.detect_syndrome(1)
    
    # Run
    result = simulator.run(transpile(qc, simulator), shots=1024).result()
    print(f"Syndrome Detected at Coordinate: {syndrome_coord}")
    print(f"Logical State Counts: {result.get_counts()}")

if __name__ == "__main__":
    run_noise_simulation()

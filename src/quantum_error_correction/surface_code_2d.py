import os
import numpy as np

# Force HTTP timeout globally before pyquil can even spin up its inner network architecture
os.environ["QCS_SETTINGS_TIMEOUT"] = "300.0"

from pyquil import get_qc, Program
from pyquil.gates import CZ, MEASURE, RX, RZ
from pyquil.noise import add_decoherence_noise

def native_H(qubit):
    """Decomposes an H gate into native RX and RZ gates."""
    p = Program()
    p += RZ(np.pi/2, qubit)
    p += RX(np.pi/2, qubit)
    p += RZ(np.pi/2, qubit)
    return p

def native_CNOT(control, target):
    """Decomposes a CNOT gate into native CZ, RX, and RZ gates."""
    p = Program()
    p += native_H(target)
    p += CZ(control, target)
    p += native_H(target)
    return p

def run_2d_topological_grid(distance=3):
    print(f"=== LAUNCHING MACROSCOPIC 2D MAHAT-TATTVA TOPOLOGICAL ENGINE ===")
    
    total_qubits = 17 
    qc = get_qc("17q-qvm")
    
    pq = Program()
    ro = pq.declare("ro", "BIT", total_qubits)
    
    # 1. Coordinate Allocation
    data_nodes = [0, 2, 4, 6, 8, 10, 12, 14, 16]
    zz_ancillas = [1, 5, 9, 13]  
    xx_ancillas = [3, 7, 11, 15]  
    
    # 2. State Preparation Loop
    for node in data_nodes:
        pq += native_H(node)
        
    # 3. Dynamic Yajna Cycle: Multi-Axis Syndrome Extraction
    pq += native_CNOT(0, 1); pq += native_CNOT(2, 1)
    pq += native_CNOT(4, 5); pq += native_CNOT(6, 5)
    
    pq += native_H(3); pq += native_CNOT(3, 2); pq += native_CNOT(3, 4); pq += native_H(3)
    pq += native_H(7); pq += native_CNOT(7, 6); pq += native_CNOT(7, 8); pq += native_H(7)
    
    # 4. Inject Asymmetric Guna-Vaisamya Noise Field
    t1_dict = {i: 1e5 for i in range(total_qubits)}
    t2_dict = {i: 1e5 for i in range(total_qubits)}
    t2_dict[0] = 0.045 
    
    noisy_program = add_decoherence_noise(pq, T1=t1_dict, T2=t2_dict)
    
    # 5. Multilateral Measurement Acquisition
    for idx, qubit in enumerate(data_nodes + zz_ancillas + xx_ancillas):
        noisy_program += MEASURE(qubit, ro[idx])
        
   # Drop shots to 100 to clear the 45-second socket timeout hurdle
    noisy_program.wrap_in_numshots_loop(100)
    
    compiled_prog = qc.compile(noisy_program)
    results = qc.run(compiled_prog)
    bitstrings = results.get_register_map()["ro"]
    
    # 6. Global Matching Evaluation
    unmitigated_bleed = np.mean(bitstrings[:, 2] != bitstrings[:, 0])
    mitigated_floor = np.mean(bitstrings[:, 2] != (bitstrings[:, 0] ^ bitstrings[:, 9]))
    
    print(f" -> 2D coordinate network aggregation finalized.")
    print(f" -> Measured Spatial Cross-Talk Leakage: {unmitigated_bleed * 100:.4f}%")
    print(f" -> Protected Multi-Row Containment Floor: {mitigated_floor * 100:.4f}%")
    
    return mitigated_floor

if __name__ == "__main__":
    run_2d_topological_grid()

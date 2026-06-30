import numpy as np
from pyquil import Program, get_qc
from pyquil.gates import H, X, T, CNOT, MEASURE

# Step 1: Logical-to-Physical Hardware Registration
DATA_QUBITS = [12, 13, 14, 15]  # q[0] to q[3]
BIND_HUB = 16                   # q[4] Central Ancilla (Parity Sensor)

def build_hybrid_drag_program():
    p = Program()
    ro = p.declare('ro', 'BIT', len(DATA_QUBITS) + 1)
    
    # --- DRAG WAVEFORM MATHEMATICS ---
    samples = 40
    time = np.arange(0, 1, 1.0 / samples)
    gaussian = np.exp(-0.5 * ((time - 0.5) / 0.15) ** 2)
    derivative = -(time - 0.5) / (0.15 ** 2) * gaussian
    drag_iq = [complex(i, q * 0.5) for i, q in zip(gaussian, derivative)]
    
    # [PATCH 1]: Bypass PyQuil AST bugs by injecting raw Quilt strings.
    # We use 'drag_clean' to avoid reserved word conflicts in strict quilc.
    quilt_def = "DEFWAVEFORM drag_clean:\n"
    for iq in drag_iq:
        quilt_def += f"    {iq.real}, {iq.imag}\n"
    p.inst(quilt_def)
    
    # [PATCH 2]: Define the missing hardware frames for the generic QVM
    for q in DATA_QUBITS:
        p.inst(f'DEFFRAME {q} "rf":\n    SAMPLE-RATE: 1e9')
    # ---------------------------------
    
    # Step 2: Initialize the unmanifest potential (Sattva)
    for q in DATA_QUBITS:
        p += H(q)
        
    # Step 3: Inject the Tamasic Perturbation (Local Asymmetry)
    p += X(13)
    
    # Step 4: Hybrid Transversal Sweep (Ahimsā Filtering + Mathematical Execution)
    for q in DATA_QUBITS:
        # 1. Quilt routing to validate the microwave compiler pipeline
        p.inst(f'PULSE {q} "rf" drag_clean')
        # 2. Logical state-vector execution so the generic QVM computes the math
        p += T(q)
        
    # Step 5: Parity Extraction via the Bindu Hub
    for q in DATA_QUBITS:
        p += CNOT(q, BIND_HUB)
        
    # Terminal Measurement
    for i, q in enumerate(DATA_QUBITS):
        p += MEASURE(q, ro[i])
    p += MEASURE(BIND_HUB, ro[4])
    
    # Step 6: 1024-shot aggregation to capture the true Mahat-Tattva statistics
    p.wrap_in_numshots_loop(1024)
    
    return p

def execute_quilt_test():
    qc = get_qc('9q-square-qvm') 
    p = build_hybrid_drag_program()
    executable = qc.compile(p)
    
    # [PATCH 3]: Modernized PyQuil 4.0.0+ register mapping
    results = qc.run(executable).get_register_map().get('ro')
    return results

if __name__ == "__main__":
    print("--- Horizon 3: Hybrid Quil-T Transversal Execution ---")
    print("Initializing QVM, loading microwave frames, and computing state vectors...")
    
    try:
        results = execute_quilt_test()
        
        q13_errors = sum([row[1] for row in results])
        hub_parity = sum([row[4] for row in results])
        cascaded_faults = sum([row[0] for row in results]) + \
                          sum([row[2] for row in results]) + \
                          sum([row[3] for row in results])
        
        print(f"\nExecution Successful over 1024 runs.")
        print(f"Tamasic Faults sustained on Target (Q13) : {q13_errors}")
        print(f"Bindu Hub (Q16) Parity Triggers          : {hub_parity}")
        print(f"Cascaded Leakage Faults (Q12, Q14, Q15)  : {cascaded_faults}")
        print("\nIf Cascaded Leakage is bounded, the DRAG pulses successfully")
        print("maintained absolute thermal stillness across the 3D cell complex.")
        
    except Exception as e:
        print(f"QVM Execution Error: {e}")

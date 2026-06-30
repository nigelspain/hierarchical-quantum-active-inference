import argparse
from qiskit.qasm3 import loads
from qiskit_aer import AerSimulator
from qiskit import transpile
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

def emulate_circuit():
    parser = argparse.ArgumentParser(description="Emulate a braided topological circuit.")
    parser.add_argument("--config", type=str, default="braided_topological_engine.qasm")
    parser.add_argument("--output", type=str)
    parser.add_argument("--phase", type=int)
    parser.add_argument("--plot", action="store_true")
    args = parser.parse_args()

    with open(args.config, "r") as f:
        qasm_str = f.read()
    
    circuit = loads(qasm_str)
    
    simulator = AerSimulator()
    compiled_circuit = transpile(circuit, simulator)
    
    result = simulator.run(compiled_circuit, shots=1024).result()
    counts = result.get_counts()
    
    print("--- Emulation Results ---")
    print(counts)

    if args.plot or args.output:
        plot_histogram(counts)
        output_filename = args.output if args.output else "emulation_result.png"
        plt.savefig(output_filename, bbox_inches='tight')
        print(f"Plot successfully saved to {output_filename}")

if __name__ == "__main__":
    emulate_circuit()

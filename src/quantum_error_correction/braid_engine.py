import stim
import numpy as np

class BraidEngine:
    def __init__(self, steps=10):
        self.steps = steps
        
    def generate_braid_step(self, step):
        # We cycle the connectivity to simulate the defect moving
        c1 = step % 3
        c2 = (step + 1) % 3
        return f"CX {c1} 4 {c2} 4"

    def run_braid(self):
        # Initializing the lattice and the puncture (Qubit 0)
        circuit_str = "R 0 1 2 3 4\n"
        
        for i in range(self.steps):
            circuit_str += f"# Braiding Step {i}\n"
            circuit_str += self.generate_braid_step(i) + "\n"
            # TICK advances the simulation clock in the 4D manifold
            circuit_str += "TICK\n" 
            
        circuit_str += """
        H 4
        M 4
        OBSERVABLE_INCLUDE(0) rec[-1]
        """
        return stim.Circuit(circuit_str)

# Execution
engine = BraidEngine(steps=10)
circuit = engine.run_braid()
sampler = circuit.compile_detector_sampler()
# We sample observables to see if the topological charge reached the end
shots = sampler.sample(shots=20, separate_observables=True)

print("--- Adiabatic Braiding Result: Final Topological Charge ---")
print(shots)

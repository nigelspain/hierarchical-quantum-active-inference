import numpy as np

class ViratRupaHierarchy:
    def __init__(self, num_subloops=2):
        self.num_subloops = num_subloops
        # L1 Global Macro State
        self.p_macro = np.random.rand(4) 
        # L0 Local Sub-loop States (Indriyas)
        self.sub_loops = [np.random.rand(4) for _ in range(num_subloops)]
        
    def structural_projection(self, a=0.3):
        """Top-down projection mapping from L1 to L0 sub-loops."""
        for i in range(self.num_subloops):
            # Modulate local Buddhi expectations using global prior [cite: 59]
            self.sub_loops[i] = (1 - a) * self.sub_loops[i] + a * self.p_macro
            
    def compute_macro_error(self):
        """Evaluate global prediction error using trace distance."""
        # Calculate trace distance between global state and local sub-loop aggregate
        sub_aggregate = np.mean(self.sub_loops, axis=0)
        e_macro = 0.5 * np.linalg.norm(self.p_macro - sub_aggregate, ord=1)
        return e_macro

# Execution and Validation
hierarchy = ViratRupaHierarchy()
print(f"{'Step':<10} | {'Global Macro Prediction Error (E)':<30}")
print("-" * 50)

for step in range(10):
    hierarchy.structural_projection(a=0.3)
    error = hierarchy.compute_macro_error()
    print(f"{step:<10} | {error:<30.4f}")

import numpy as np

class AdaptiveCognitiveEngine:
    def __init__(self, t_boundary=5.0, w=0.5):
        self.t_boundary = t_boundary  # Epoch transition point
        self.w = w  # Transition width
        self.phi = np.zeros(3)  # Hidden state variables (Samskāras)
        
    def get_tau(self, t):
        """Adiabatic Sandhyā Scheduler modulating time constants."""
        # Sigmoidal partition of unity for smooth epochal transitions
        W_B = 1.0 / (1.0 + np.exp(-(t - self.t_boundary) / self.w))
        tau_A = np.array([0.1, 1.0, 10.0])  # Winter phase constants
        tau_B = np.array([0.5, 5.0, 50.0])  # Spring phase constants
        return (1.0 - W_B) * tau_A + W_B * tau_B

    def update(self, t, rho_sub, dt):
        """Recursive update for the Chitta reservoir."""
        tau = self.get_tau(t)
        # Update hidden states: d(phi)/dt = -phi/tau + rho_sub
        self.phi += (-self.phi / tau + rho_sub) * dt
        # Current Chitta state projection
        return np.sum(self.phi)

# Execution block
engine = AdaptiveCognitiveEngine(t_boundary=5.0)
dt = 0.1
print(f"{'Time (t)':<10} | {'Chitta State':<15}")
print("-" * 25)

for t in np.linspace(0, 10, 20):
    rho_sub = np.sin(t)  # Time-dependent perturbation
    chitta_state = engine.update(t, rho_sub, dt)
    print(f"{t:<10.2f} | {chitta_state:<15.4f}")

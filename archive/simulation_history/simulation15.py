import numpy as np

class AdaptiveCognitiveEngine:
    def __init__(self, t_boundary=5.0, w=0.5):
        self.t_boundary = t_boundary
        self.w = w
        self.phi = np.zeros(3)  # Hidden state variables (Samskāras)
        
    def get_tau(self, t):
        """Adiabatic Sandhyā Scheduler modulating time constants[cite: 66]."""
        W_B = 1.0 / (1.0 + np.exp(-(t - self.t_boundary) / self.w))
        tau_A = np.array([0.1, 1.0, 10.0])
        tau_B = np.array([0.5, 5.0, 50.0])
        return (1.0 - W_B) * tau_A + W_B * tau_B

    def update(self, t, rho_sub, dt, E, D_threshold=0.5):
        """Recursive update with integrated Bhakti-bīja neutralization[cite: 79, 81]."""
        # Dynamic Bhakti-bīja trigger: if systemic uncertainty exceeds threshold
        if E > D_threshold:
            self.phi = np.zeros_like(self.phi)  # Absolute history neutralization
            return 0.0
        
        tau = self.get_tau(t)
        # Update hidden states: d(phi)/dt = -phi/tau + rho_sub [cite: 73, 75]
        self.phi += (-self.phi / tau + rho_sub) * dt
        return np.sum(self.phi)

# Execution block
engine = AdaptiveCognitiveEngine(t_boundary=5.0)
dt = 0.1
print(f"{'Time (t)':<10} | {'E (Uncertainty)':<16} | {'Chitta State':<15}")
print("-" * 45)

for t in np.linspace(0, 10, 20):
    rho_sub = np.sin(t)
    # Simulated prediction error (E) peaking around t=5.0 [cite: 153]
    E = abs(np.sin(t) * 0.8) 
    chitta_state = engine.update(t, rho_sub, dt, E, D_threshold=0.4)
    print(f"{t:<10.2f} | {E:<16.4f} | {chitta_state:<15.4f}")

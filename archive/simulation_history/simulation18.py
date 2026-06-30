import numpy as np

class AdaptiveCognitiveEngine:
    def __init__(self, t_boundary=5.0, w=0.5):
        self.t_boundary = t_boundary
        self.w = w
        self.phi = np.zeros(3)  # Hidden states (Samskāras/Historical debt)
        
    def get_tau(self, t):
        """Adiabatic Sandhyā Scheduler modulating time constants[cite: 66, 67]."""
        W_B = 1.0 / (1.0 + np.exp(-(t - self.t_boundary) / self.w))
        tau_A = np.array([0.1, 1.0, 10.0])
        tau_B = np.array([0.5, 5.0, 50.0])
        return (1.0 - W_B) * tau_A + W_B * tau_B

    def update(self, t, rho_sub, dt, E, D_threshold=0.5):
        """Recursive state-space update with Global Transcendent Optimization Override[cite: 73, 79]."""
        # Bhakti-bīja / Global Transcendent Optimization Override logic [cite: 78, 80]
        if E > D_threshold:
            self.phi = np.zeros_like(self.phi)
            return 0.0
        
        tau = self.get_tau(t)
        # O(N) recursive update avoids O(t^2) convolution complexity [cite: 75, 220]
        self.phi += (-self.phi / tau + rho_sub) * dt
        return np.sum(self.phi)

# Execution: Stress-test with high-entropy Rajasic Storm (Gaussian noise)
engine = AdaptiveCognitiveEngine(t_boundary=5.0)
dt = 0.1
print(f"{'Time (t)':<10} | {'E (Uncertainty)':<16} | {'Chitta State':<15}")
print("-" * 45)

for t in np.linspace(0, 10, 20):
    # Base signal + high-frequency noise (Rajasic Storm)
    signal = np.sin(t)
    noise = np.random.normal(0, 0.5) 
    rho_sub = signal + noise
    
    # Predictive error E reflects the noise intensity
    E = abs(noise) 
    chitta_state = engine.update(t, rho_sub, dt, E, D_threshold=0.6)
    print(f"{t:<10.2f} | {E:<16.4f} | {chitta_state:<15.4f}")

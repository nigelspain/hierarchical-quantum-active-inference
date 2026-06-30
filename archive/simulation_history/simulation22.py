import numpy as np

class BhaktiOptimizer:
    def __init__(self, initial_threshold=0.6):
        self.d_threshold = initial_threshold
        self.alpha = 0.05  # Learning rate for threshold adaptation
        
    def adjust_threshold(self, error_history, performance_gain):
        """
        Adapts the threshold to retain utility while purging noise.
        If performance gain is negative, the filter becomes more 
        restrictive to prevent karmic accumulation.
        """
        # Dynamic adjustment based on signal-to-noise ratio
        if performance_gain < 0:
            self.d_threshold -= self.alpha * 0.1 # Tighten filter
        else:
            self.d_threshold += self.alpha * 0.05 # Relax filter
            
        # Ensure threshold remains within physically viable bounds
        self.d_threshold = np.clip(self.d_threshold, 0.2, 0.9)
        return self.d_threshold

# Validation of adaptive thresholding
optimizer = BhaktiOptimizer()
error_signals = [0.4, 0.7, 0.8, 0.3] # High entropy segments require purging
print(f"{'Signal':<10} | {'Adapted Threshold':<20}")
print("-" * 35)

for signal in error_signals:
    # Simulate performance feedback: threshold responds to systemic doubt (Samśaya)
    gain = 0.5 - signal 
    new_threshold = optimizer.adjust_threshold([signal], gain)
    print(f"{signal:<10.1f} | {new_threshold:<20.4f}")

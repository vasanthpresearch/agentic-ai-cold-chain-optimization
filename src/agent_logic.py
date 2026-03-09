import numpy as np

class ColdChainAgent:
    def __init__(self, temp_threshold=5.0, rsl_threshold=0.8):
        self.temp_threshold = temp_threshold
        self.rsl_threshold = rsl_threshold # Residual Shelf Life

    def calculate_kinetic_degradation(self, temp_c):
        """
        Simplified Arrhenius Logic: Calculates the quality loss 
        based on temperature kinetic energy.
        """
        # Reaction rate increases exponentially with temperature
        k = np.exp(0.1 * (temp_c - 2.0)) 
        return k

    def evaluate_action(self, predicted_temp):
        """
        The Agentic Decision: Should we reroute the truck?
        """
        degradation_rate = self.calculate_kinetic_degradation(predicted_temp)
        
        if predicted_temp > self.temp_threshold or degradation_rate > 1.5:
            return "🚨 ACTION REQUIRED: Reroute to nearest MFC (Micro-Fulfillment Center)"
        else:
            return "✅ STATUS: Optimal. Continue to original destination."

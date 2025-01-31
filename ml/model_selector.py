# ml/model_selector.py

from ml.model_interfaces import IMLModel

# Placeholder classes for demonstration. In a real implementation,
# RandomForestModel and DeepRLModel would be imported from their respective modules.
class RandomForestModel(IMLModel):
    def predict_action(self, features):
        return "BUY"  # Placeholder logic

class DeepRLModel(IMLModel):
    def predict_action(self, features):
        return "HOLD"  # Placeholder logic

def get_ml_model(config: dict) -> IMLModel:
    """
    Returns an instance of an IMLModel based on the 'ml_model' key in the config.
    """
    ml_model_type = config.get("ml_model", "random_forest")

    if ml_model_type == "random_forest":
        return RandomForestModel()
    elif ml_model_type == "deep_rl":
        return DeepRLModel()
    else:
        raise ValueError(f"Unknown ML model type: {ml_model_type}")

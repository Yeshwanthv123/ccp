import tensorflow as tf
import numpy as np
from PIL import Image
import os
import json
from typing import Dict, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SignageClassifier:
    """
    A classifier that trains on SYNTHETIC data for demonstration purposes.
    This model learns to differentiate between a horizontal and a vertical stripe.
    """
    def __init__(self, model_path: str = "models/signage_classifier.h5"):
        self.model_path = model_path
        self.model = None
        # This model is for a BINARY classification task
        self.class_names = ["unauthorized", "authorized"]
        self.input_shape = (224, 224, 3)

    def create_model(self) -> tf.keras.Model:
        """Create a CNN model for binary classification."""
        model = tf.keras.Sequential([
            tf.keras.layers.Rescaling(1./255, input_shape=self.input_shape),
            tf.keras.layers.Conv2D(16, 3, padding='same', activation='relu'),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Conv2D(32, 3, padding='same', activation='relu'),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Conv2D(64, 3, padding='same', activation='relu'),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(128, activation='relu'),
            # Use 1 neuron and sigmoid for binary classification
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])

        model.compile(
            optimizer='adam',
            loss='binary_crossentropy', # Use binary_crossentropy for two classes
            metrics=['accuracy']
        )
        return model

    def generate_synthetic_data(self, num_samples: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
        """Generate synthetic training data."""
        logger.info(f"Generating {num_samples} synthetic training samples...")
        X = np.random.rand(num_samples, *self.input_shape).astype(np.float32) * 150.0
        y = np.random.randint(0, 2, num_samples)

        for i in range(num_samples):
            # Class 1 ("authorized"): Add a distinct horizontal feature
            if y[i] == 1:
                X[i, 100:124, 50:174, :] = 255.0 # Bright horizontal stripe
            # Class 0 ("unauthorized"): Add a distinct vertical feature
            else:
                X[i, 50:174, 100:124, :] = 255.0 # Bright vertical stripe
        
        return X, y

    def train_model(self, epochs: int = 15, **kwargs): # Added **kwargs to accept unused arguments
        """Train the model on synthetically generated data."""
        logger.info("Starting model training on synthetic data...")

        self.model = self.create_model()
        X, y = self.generate_synthetic_data(num_samples=1000)

        history = self.model.fit(
            X, y,
            epochs=epochs,
            validation_split=0.2,
            batch_size=32,
            verbose=1
        )

        os.makedirs("models", exist_ok=True)
        self.model.save(self.model_path)
        
        with open("models/training_history.json", "w") as f:
            json.dump({k: [float(val) for val in v] for k, v in history.history.items()}, f)
        
        with open("models/class_names.json", "w") as f:
            json.dump(self.class_names, f)

        logger.info(f"Synthetic model training completed and saved to {self.model_path}")
        return history

    def load_model(self):
        """Load the model, or train a new one if it doesn't exist."""
        if os.path.exists(self.model_path):
            logger.info(f"Loading model from {self.model_path}")
            self.model = tf.keras.models.load_model(self.model_path)
            class_names_path = "models/class_names.json"
            if os.path.exists(class_names_path):
                with open(class_names_path, "r") as f:
                    self.class_names = json.load(f)
        else:
            logger.warning("No pre-trained model found. Training a new synthetic model...")
            self.train_model()

    def preprocess_image(self, image: Image.Image) -> np.ndarray:
        """Preprocess an image for prediction."""
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image = image.resize((self.input_shape[0], self.input_shape[1]))
        img_array = np.array(image, dtype=np.float32)
        img_array = np.expand_dims(img_array, axis=0)
        return img_array

    def predict(self, image: Image.Image) -> Dict[str, any]:
        """Predicts 'authorized' or 'unauthorized' based on synthetic features."""
        try:
            if self.model is None:
                self.load_model()

            processed_image = self.preprocess_image(image)
            prediction_prob = self.model.predict(processed_image, verbose=0)[0][0]

            predicted_class_index = 1 if prediction_prob > 0.5 else 0
            confidence = prediction_prob if predicted_class_index == 1 else (1 - prediction_prob)
            result = self.class_names[predicted_class_index]

            message = f"Model prediction: '{result}' with {confidence*100:.1f}% confidence. (Note: Based on synthetic data)."

            return {
                "prediction": result,
                "confidence": float(confidence),
                "message": message
            }
        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}")
            return {"prediction": "error", "confidence": 0.0, "message": f"Error processing image: {str(e)}"}

# Global instance of the classifier
classifier = SignageClassifier()

def get_classifier() -> SignageClassifier:
    return classifier

def initialize_model():
    """Initializes the model on application startup."""
    try:
        logger.info("Initializing AI model...")
        classifier.load_model()
        logger.info("AI model initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize AI model: {str(e)}")
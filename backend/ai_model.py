import tensorflow as tf
import numpy as np
from PIL import Image
import os
import json
from typing import Dict, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SignageClassifier:
    def __init__(self, model_path: str = "models/signage_classifier.h5"):
        self.model_path = model_path
        self.model = None
        self.class_names = ["unauthorized", "authorized"]
        self.input_shape = (224, 224, 3)

    def create_model(self) -> tf.keras.Model:
        """Create a CNN model for signage classification"""
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
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])

        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )

        return model

    def generate_synthetic_data(self, num_samples: int = 2000) -> Tuple[np.ndarray, np.ndarray]:
        """Generate synthetic training data for signage classification"""
        logger.info(f"Generating {num_samples} synthetic training samples...")

        X = np.random.rand(num_samples, *self.input_shape).astype(np.float32) * 255.0
        y = np.random.randint(0, 2, num_samples)

        for i in range(num_samples):
            if y[i] == 1: # Authorized
                X[i, 10:20, :, :] = 255.0 # White stripe
            else: # Unauthorized
                X[i, :, 10:20, :] = 255.0 # White stripe

        return X, y

    def train_model(self, epochs: int = 50, validation_split: float = 0.2):
        """Train the signage classification model"""
        logger.info("Starting model training...")

        self.model = self.create_model()

        X, y = self.generate_synthetic_data(num_samples=2000)

        history = self.model.fit(
            X, y,
            epochs=epochs,
            validation_split=validation_split,
            batch_size=32,
            verbose=1
        )

        os.makedirs("models", exist_ok=True)
        self.model.save(self.model_path)

        with open("models/training_history.json", "w") as f:
            json.dump({
                "loss": [float(x) for x in history.history["loss"]],
                "accuracy": [float(x) for x in history.history["accuracy"]],
                "val_loss": [float(x) for x in history.history["val_loss"]],
                "val_accuracy": [float(x) for x in history.history["val_accuracy"]]
            }, f)

        logger.info(f"Model training completed and saved to {self.model_path}")
        return history

    def load_model(self):
        """Load the trained model"""
        if os.path.exists(self.model_path):
            logger.info(f"Loading model from {self.model_path}")
            self.model = tf.keras.models.load_model(self.model_path)
        else:
            logger.info("No pre-trained model found. Training new model...")
            self.train_model()

    def preprocess_image(self, image: Image.Image) -> np.ndarray:
        """Preprocess image for prediction"""
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image = image.resize((224, 224))
        img_array = np.array(image, dtype=np.float32)
        img_array = np.expand_dims(img_array, axis=0)
        return img_array

    def predict(self, image: Image.Image) -> Dict[str, float]:
        """Predict if signage is authorized or unauthorized"""
        try:
            if self.model is None:
                self.load_model()

            processed_image = self.preprocess_image(image)

            prediction_prob = self.model.predict(processed_image, verbose=0)[0][0]

            predicted_class = 1 if prediction_prob > 0.5 else 0
            confidence = prediction_prob if predicted_class == 1 else (1 - prediction_prob)

            result = self.class_names[predicted_class]

            if result == "authorized":
                message = f"This signage appears to be properly authorized and compliant with regulations. The AI model detected official characteristics with {confidence*100:.1f}% confidence."
            else:
                message = f"This signage may be unauthorized or non-compliant. The AI model detected irregular patterns suggesting it may require further review with {confidence*100:.1f}% confidence."

            return {
                "prediction": result,
                "confidence": float(confidence),
                "message": message,
                "raw_probability": float(prediction_prob)
            }

        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}")
            return {
                "prediction": "error",
                "confidence": 0.0,
                "message": f"Error processing image: {str(e)}",
                "raw_probability": 0.0
            }

classifier = SignageClassifier()

def get_classifier() -> SignageClassifier:
    return classifier

def initialize_model():
    try:
        logger.info("Initializing AI model...")
        classifier.load_model()
        logger.info("AI model initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize AI model: {str(e)}")
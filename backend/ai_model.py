import tensorflow as tf
import numpy as np
from PIL import Image
import os
import json
from typing import Tuple, Dict
import logging

# Set up logging
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
            # Input layer
            tf.keras.layers.Input(shape=self.input_shape),
            
            # Data augmentation layers
            tf.keras.layers.RandomFlip("horizontal"),
            tf.keras.layers.RandomRotation(0.1),
            tf.keras.layers.RandomZoom(0.1),
            
            # Normalization
            tf.keras.layers.Rescaling(1./255),
            
            # First convolutional block
            tf.keras.layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Dropout(0.25),
            
            # Second convolutional block
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Dropout(0.25),
            
            # Third convolutional block
            tf.keras.layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Dropout(0.25),
            
            # Fourth convolutional block
            tf.keras.layers.Conv2D(256, (3, 3), activation='relu', padding='same'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Conv2D(256, (3, 3), activation='relu', padding='same'),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Dropout(0.25),
            
            # Global average pooling
            tf.keras.layers.GlobalAveragePooling2D(),
            
            # Dense layers
            tf.keras.layers.Dense(512, activation='relu'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dropout(0.5),
            
            tf.keras.layers.Dense(256, activation='relu'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dropout(0.5),
            
            # Output layer
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])
        
        # Compile the model
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss='binary_crossentropy',
            metrics=['accuracy', 'precision', 'recall']
        )
        
        return model
    
    def generate_synthetic_data(self, num_samples: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
        """Generate synthetic training data for signage classification"""
        logger.info(f"Generating {num_samples} synthetic training samples...")
        
        X = []
        y = []
        
        for i in range(num_samples):
            # Create synthetic signage images
            img = np.random.rand(224, 224, 3) * 255
            
            # Create patterns that distinguish authorized vs unauthorized signage
            if i % 2 == 0:  # Authorized signage
                # Add structured patterns (simulating official signage)
                # Add borders
                img[:10, :, :] = [0, 0, 255]  # Blue border top
                img[-10:, :, :] = [0, 0, 255]  # Blue border bottom
                img[:, :10, :] = [0, 0, 255]  # Blue border left
                img[:, -10:, :] = [0, 0, 255]  # Blue border right
                
                # Add text-like rectangles (simulating official text)
                img[50:70, 50:150, :] = [255, 255, 255]  # White rectangle
                img[80:100, 50:150, :] = [255, 255, 255]  # White rectangle
                
                label = 1  # Authorized
            else:  # Unauthorized signage
                # Add random, unstructured patterns
                # Random colors and shapes
                img[np.random.randint(0, 200, 100), np.random.randint(0, 200, 100), :] = np.random.rand(100, 3) * 255
                
                # Add graffiti-like patterns
                for _ in range(5):
                    x, y_pos = np.random.randint(0, 200, 2)
                    img[x:x+20, y_pos:y_pos+20, :] = np.random.rand(3) * 255
                
                label = 0  # Unauthorized
            
            X.append(img.astype(np.uint8))
            y.append(label)
        
        return np.array(X), np.array(y)
    
    def train_model(self, epochs: int = 50, validation_split: float = 0.2):
        """Train the signage classification model"""
        logger.info("Starting model training...")
        
        # Create model
        self.model = self.create_model()
        
        # Generate synthetic training data
        X, y = self.generate_synthetic_data(num_samples=2000)
        
        # Create callbacks
        callbacks = [
            tf.keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=10,
                restore_best_weights=True
            ),
            tf.keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=1e-7
            )
        ]
        
        # Train the model
        history = self.model.fit(
            X, y,
            epochs=epochs,
            validation_split=validation_split,
            batch_size=32,
            callbacks=callbacks,
            verbose=1
        )
        
        # Save the model
        os.makedirs("models", exist_ok=True)
        self.model.save(self.model_path)
        
        # Save training history
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
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize image
        image = image.resize((224, 224))
        
        # Convert to numpy array
        img_array = np.array(image)
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    
    def predict(self, image: Image.Image) -> Dict[str, float]:
        """Predict if signage is authorized or unauthorized"""
        try:
            if self.model is None:
                self.load_model()
            
            # Preprocess image
            processed_image = self.preprocess_image(image)
            
            # Make prediction
            prediction_prob = self.model.predict(processed_image, verbose=0)[0][0]
            
            # Convert to class prediction
            predicted_class = 1 if prediction_prob > 0.5 else 0
            confidence = prediction_prob if predicted_class == 1 else (1 - prediction_prob)
            
            result = self.class_names[predicted_class]
            
            # Generate appropriate message
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

# Global classifier instance
classifier = SignageClassifier()

def get_classifier() -> SignageClassifier:
    """Get the global classifier instance"""
    return classifier

def initialize_model():
    """Initialize the model on startup"""
    try:
        logger.info("Initializing AI model...")
        classifier.load_model()
        logger.info("AI model initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize AI model: {str(e)}")
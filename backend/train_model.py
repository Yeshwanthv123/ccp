#!/usr/bin/env python3
"""
Script to train the signage classification model
Run this script to train the AI model before starting the server
"""

import os
import sys
from ai_model import SignageClassifier
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Train the signage classification model"""
    logger.info("Starting signage classification model training...")
    
    # Create classifier instance
    classifier = SignageClassifier()
    
    # Train the model
    try:
        history = classifier.train_model(epochs=50, validation_split=0.2)
        
        # Print training results
        final_accuracy = history.history["accuracy"][-1]
        final_val_accuracy = history.history["val_accuracy"][-1]
        final_loss = history.history["loss"][-1]
        final_val_loss = history.history["val_loss"][-1]
        
        logger.info("Training completed successfully!")
        logger.info(f"Final Training Accuracy: {final_accuracy:.4f}")
        logger.info(f"Final Validation Accuracy: {final_val_accuracy:.4f}")
        logger.info(f"Final Training Loss: {final_loss:.4f}")
        logger.info(f"Final Validation Loss: {final_val_loss:.4f}")
        
        # Test the model with a sample prediction
        logger.info("Testing model with sample prediction...")
        from PIL import Image
        import numpy as np
        
        # Create a test image
        test_image = Image.fromarray(np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8))
        result = classifier.predict(test_image)
        
        logger.info(f"Sample prediction: {result['prediction']} (confidence: {result['confidence']:.4f})")
        logger.info("Model is ready for use!")
        
    except Exception as e:
        logger.error(f"Training failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
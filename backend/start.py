import uvicorn
import os
import multiprocessing
from ai_model import initialize_model
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_fastapi():
    """Start the FastAPI server"""
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

def run_model_initialization():
    """Initialize and train the AI model"""
    logger.info("Starting AI model initialization in a separate process...")
    initialize_model()
    logger.info("AI model initialization process finished.")

if __name__ == "__main__":
    # Set environment variables for development
    os.environ["DATABASE_URL"] = "postgresql://user:password@db:5432/urban_guard_db"
    
    # Create processes for the FastAPI app and model training
    fastapi_process = multiprocessing.Process(target=run_fastapi)
    model_process = multiprocessing.Process(target=run_model_initialization)
    
    # Start both processes
    fastapi_process.start()
    model_process.start()
    
    # Join processes to keep the main script running
    fastapi_process.join()
    model_process.join()
import logging

# Configure logging
logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_message(message, level="info"):
    if level == "info":
        logging.info(message)
    elif level == "warning":
        logging.warning(message)
    elif level == "error":
        logging.error(message)

# Example usage
if __name__ == "__main__":
    log_message("Pipeline started")
    try:
        # Your code here
        pass
    except Exception as e:
        log_message(f"Error: {str(e)}", level="error")

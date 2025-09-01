import logging

logging.basicConfig(
    level=logging.DEBUG,    # Set the logging level to DEBUG
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Define the log message format
)

logging.debug("This is a debug message")
logging.info("This is an info message")
logging.warning("This is a warning message")
logging.error("This is an error message")   
logging.critical("This is a critical message")
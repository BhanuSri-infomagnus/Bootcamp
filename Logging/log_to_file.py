import logging

# Create a custom logger named "MyLogger"
logger = logging.getLogger("MyLogger")
logger.setLevel(logging.DEBUG)  # Set minimum log level to DEBUG (captures all levels)

# Create a file handler to write logs to 'app.log'
# 'w' mode overwrites the log file each time the script runs
file_handler = logging.FileHandler("app.log", mode='w')

# Define a log message format: timestamp, log level, and message
file_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Attach the formatter to the file handler
file_handler.setFormatter(file_format)

# Add the file handler to the logger
logger.addHandler(file_handler)

# Example function that uses the logger to record events and errors
def divide(a, b):
    logger.info(f"Trying to divide {a} by {b}")  # Log the operation at INFO level
    try:
        result = a / b
        logger.debug(f"Result: {result}")  # Log the result at DEBUG level
        return result
    except ZeroDivisionError:
        # Log an error message with exception info if division by zero occurs
        logger.error("Cannot divide by zero", exc_info=True)
        return None

# Run some test calls to demonstrate logging
divide(10, 2)  # Should log INFO and DEBUG messages
divide(5, 0)   # Should log INFO and ERROR messages due to division by zero

# Log a WARNING message
logger.warning("This is just a test warning")

# Log a CRITICAL message
logger.critical("Critical issue happened!")
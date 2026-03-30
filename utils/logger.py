import logging

def setup_logger():
    logger=logging.getLogger()
    logger.setLevel(logging.INFO)
    
    #console Handler
    console_handler=logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    #File Handler
    file_handler=logging.FileHandler()
    file_handler.setLevel(logging.INFO)
    
    #format
    formatter=logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
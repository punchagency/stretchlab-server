import logging

def setup_logging(log_file='app.log', level=logging.DEBUG):
    logging.basicConfig(
        filename=log_file,
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
import logging 
import os 

log_path=os.path.join(os.getcwd(),'logs')

filename=os.path.join(log_path,'logs.log')

def setup_logging(message,level=logging.INFO):
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename=filename
    )

    if level==logging.INFO:
        logging.info(message)
    if level==logging.DEBUG:
        logging.debug(message)
    if level==logging.CRITICAL:
        logging.critical(message)
    if level==logging.WARN:
        logging.warning(message)
import logging

def setup_logging(log_path=None):
    format_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_fmt_str = '%Y-%m-%d %H:%M:%S'
    logging.basicConfig(level=logging.INFO,
                        format=format_str,
                        datefmt=date_fmt_str)
    
    if log_path:
        file_handler = logging.FileHandler(log_path)
        file_formatter = logging.Formatter(format_str, datefmt=date_fmt_str)
        file_handler.setFormatter(file_formatter)
        logging.getLogger().addHandler(file_handler)

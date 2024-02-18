import sys
import os
import argparse
import logging

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
src_path = os.path.join(project_root, 'src')
sys.path.append(src_path)

from util import config_loader
from util.logger_config import setup_logging
from util.db_manager import init_db
from harvester import harvester

def set_parser():
    parser = argparse.ArgumentParser(description="Example script with logging option.")
    default_log_path = os.path.join(os.path.dirname(__file__), '..', '..', 'log', 'app.log')
    parser.add_argument("--log", help="Specify the log file path.", default=default_log_path)

    return parser

def main():
    parser = set_parser()
    args = parser.parse_args()

    setup_logging(args.log)

    config = config_loader.load_config()
    keys = config['api_keys']
    key = keys[0]

    logging.info(f"API key: {key}")
    init_db()
    harvester(key)

if __name__ == "__main__":
    main()
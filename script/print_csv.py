import sys
import os
import argparse

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_path = os.path.join(project_root, 'src')
sys.path.append(src_path)

from util.csv_manager import read_and_print_champion_names_from_csv

def main():
    parser = argparse.ArgumentParser(description="print csv file.")
    parser.add_argument("start", help="Specify the start line.", type=int, default=0)
    parser.add_argument("end", help="Specify the end line.", type=int, default=20)

    read_and_print_champion_names_from_csv('../results/data.csv', line_start=0, line_end=20)

if __name__ == '__main__':
    main()
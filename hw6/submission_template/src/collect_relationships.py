import bs4 
import json 
import argparse
import requests
import os.path


def get_args(): 
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', type=str)
    parser.add_argument('-o', '--output', type=str)

    return parser.parse_args().config, parser.parse_args().output

def main(): 

    config_file, output_file = get_args()


if __name__ == "__main__": 
    main() 
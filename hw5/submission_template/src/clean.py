import json 
import argparse

def get_args(): 
    parser = argparse.ArgumentParser() 
    parser.add_argument('-i', '--input', type=str)
    parser.add_argument('-o', '--output', type=str)

    return parser.parse_args().input, parser.parse_args().output
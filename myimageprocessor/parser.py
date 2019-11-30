from argparse import ArgumentParser
from pathlib import Path


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("source", type=Path)
    return parser.parse_args()

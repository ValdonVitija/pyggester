#pylint:disable=E0611
import argparse
from pyggester import pyggester

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--file", help="input file name")
    args = parser.parse_args()
    file_ = args.file
    return file_


def main():
    pyggester.suggest_refactor(parse_args())

# if __name__ == "__main__":
    # pyggester.suggest_refactor(parse_args())
# pylint:disable=E0611
import argparse
from pyggester import pyggester


def parse_args():
    """
    This function needs to be extended further. Since this is a command-line tool
    it needs to be filled with feature flags to change the behaviour of the program
    without changing the code itself.
    If this project gets continued, the number of possible arguments can be way more than one,
    so it is better to refactor this function, to decompose it into different functions or maybe
    abstract into a class
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="input file name")
    args = parser.parse_args()
    file_ = args.file
    return file_


def main():
    suggester = pyggester.CodeSuggester()
    suggester.suggest_refactor(parse_args())

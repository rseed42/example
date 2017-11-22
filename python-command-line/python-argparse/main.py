#!/usr/bin/python
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Argument Parser")
    # Positional argument, specify number of arguments
    parser.add_argument('cfg', help='Configuration file')
    # Option
    parser.add_argument('--num', '-n', action='store', default=10, help='Number of messages')
    # Boolean option
    parser.add_argument('--verbose', '-v', action='store_true', dest='verbose', default=False, help='verbosity level')
    args = parser.parse_args()
    # Show results
    print(args)

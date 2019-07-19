"""list_diff.py take two sets and compare the delta."""

import sys
from file_parser import file_to_list


def main():
    if len(sys.argv) == 3:
        file_a = sys.argv[1]
        file_b = sys.argv[2]
        print('file A is > ' + file_a)
        print('file B is > ' + file_b)
        list_a = file_to_list(file_a)
        list_b = file_to_list(file_b)
        list_a_diff_b = set(list_a) - set(list_b)
        list_b_diff_a = set(list_b) - set(list_a)
        diff_a = len(list_a_diff_b)
        diff_b = len(list_b_diff_a)
        if diff_a == 0 and diff_b == 0:
            print('No diff, two sets are containing the same items.')
        if diff_a > 0:
            print('file A contains ' + str(diff_a) + ' items which are not in file B: ')
            print(list_a_diff_b)
        if diff_b > 0:
            print('file B contains ' + str(diff_b) + ' items which are not in file A: ')
            print(list_b_diff_a)
    else:
        print('Please specify two files to be diffed!!!')


if __name__ == "__main__":
    main()

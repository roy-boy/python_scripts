"""list_merge.py merges two sets and save them into a file."""

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
        set_a = set(list_a)
        set_b = set(list_b)
        set_c = set_a.union(set_b)
        try:
            with open('file_C.txt', 'w') as out_put:
                out_put.write(str(set_c))
                print('Merging two list into one...')
        except OSError as err:
            print('Failed to open the file as ', err)
    else:
        print('Please specify two files to be merged!!!')


if __name__ == "__main__":
    main()

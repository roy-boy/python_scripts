"""file_parser.py reads text file and parse the item into a list."""


def file_to_list(input_file):
    data_list_trim = []
    try:
        with open(input_file) as in_put:
            input_data = in_put.readlines()
            if len(input_data) == 1:
                print()
                data_list = input_data[0].replace('"', '').strip()
                data_list_trim = data_list.split(',')
            elif len(input_data) > 1:
                print()
                for row in input_data:
                    row_list = row.replace('"', '').strip()
                    row_list_trim = row_list.split(',')
                    data_list_trim = data_list_trim + row_list_trim
            else:
                print('no content is the file')
    except OSError as err:
        print('Failed to open file', err)
    return data_list_trim

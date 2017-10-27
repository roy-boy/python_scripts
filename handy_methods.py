# to check the 1st/second largest item in a list, sorting a list without sort()
def second_largest(test_list):
    first, second = None, None
    for n in test_list:
        if n > first:
            print('bigger one: ' + str(n))
            first, second = n, first
    # return first
    return second


def compare_dates(utc_date, local_date):
    """take two input date format and convert gwml_date(local) to UTC
    :param utc_date
    :param local_date
    :return:
        a string passed or failed
    """
    utc_tz = tz.gettz('UTC')  # get the timezone
    fix_date_new = parse(utc_date)
    fix_date_time = fix_date_new.strftime('%Y-%m-%d %H:%M:%S')  # format the time stamp
    gwml_date_new = parse(local_date)
    gwml_date_utc = gwml_date_new.astimezone(utc_tz)  # convert to UTC time
    gwml_date_time = gwml_date_utc.strftime('%Y-%m-%d %H:%M:%S')  # format the time stamp
    if fix_date_time == gwml_date_time:
        log_test_output('Date matches.')
        return 'passed'
    else:
        log_test_output('tag value diff in FIX: ' + fix_date_time + ' <---> value in GWML: ' + gwml_date_time)
        return 'failed'

    
# to do a count on the letter in a string
def find_duplicates(string):
    search_result = {}
    test_list = list(string)
    first_letter, second_letter = None, None
    for letter in test_list:
        first_letter, second_letter = letter, first_letter
        if first_letter != second_letter:
            count = 1
            # print('letters: ' + letter)
        else:
            count += 1
            # print(count)
        search_result[letter] = count
    return search_result

# count the dup letter in a string
def letter_count(test_string):
    string_list = list(test_string)
    letter_dict = {}
    for letter in string_list:
        try:
            letter_dict[letter] += 1
        except KeyError:
            letter_dict[letter] = 1
    return letter_dict

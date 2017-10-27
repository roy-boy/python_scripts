# to check the 1st/second largest item in a list, sorting a list without sort()
def second_largest(test_list):
    first, second = None, None
    for n in test_list:
        if n > first:
            print('bigger one: ' + str(n))
            first, second = n, first
    # return first
    return second

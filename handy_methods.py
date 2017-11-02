# List Comprehension
item = [n*2 for n in range(10)]
print item

#Dict Comprehension
item = {n: n*2 for n in range(10)}
print item 

# to check the second largest item in a list, sorting a list without sort()
def second_largest(test_list):
    first, second = None, None
    for n in test_list:
        if n > first:
            print('bigger one: ' + str(n))
            first, second = n, first
    # return first
    return second


# to check the largest item in a list, sorting a list without sort()
def find_biggest(a_list):
    result = a_list[0]
    for n in a_list:
        if n > result:
            result = n
    print(result)


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


# Fibonacci numbers module
 def fib(n):    # write Fibonacci series up to n
     a, b = 0, 1
     while b < n:
         print(b, end=' ')
         a, b = b, a+b
     print()
 
 def fib2(n):   # return Fibonacci series up to n
     result = []
     a, b = 0, 1
     while b < n:
         result.append(b)
         a, b = b, a+b
     return result


# A program to count the number of ways to reach n'th stair
 
# Recursive function used by countWays
def countWaysUtil(n,m):
    res = [0 for x in range(n)] # Creates list res witth all elements 0
    res[0],res[1] = 1,1
     
    for i in range(2,n):
        j = 1
        while j<=m and j<=i:
            res[i] = res[i] + res[i-j]
            j = j + 1
    return res[n-1]
 
# Returns number of ways to reach s'th stair
def countWays(s,m):
    return countWaysUtil(s+1, m)
     
# Driver Program
s,m = 4,2
print "Nmber of ways =",countWays(s,m)
     
# Contributed by Harshit Agrawal

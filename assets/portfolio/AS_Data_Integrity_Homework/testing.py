########################################################################
# Testing module for data integrity techniques
# This module contains test cases for the functions defined in techniques.py.
# Just run it after implementing each function to verify correctness.
# Proceed to next function only if your function passes the tests.
# Your assignment is completed when you pass all tests.
########################################################################

import techniques_full as techniques

class NotImplementedYet(Exception):
    pass

def report(test_name, case_desc, got, expected):
    status = "PASS" if got == expected else "FAIL"
    print(f"""{test_name}: [{case_desc}] {status} 
    got=     {got} 
    expected={expected}""")

def ensure_return(value, func_name):
    if value is None:
        raise NotImplementedYet(f"{func_name} returned None (not implemented)")
    return value

def notify_test_start(test_func):
    print("========================================")
    print("Starting next test : ", test_func.__name__, "\n")

def notify_test_success(test_func):
    print(f"\n{test_func.__name__}: All test cases passed!")
    print("========================================\n")


test_list = []

# Test cases for range_check
def test_range_check():
    func_name = "range_check"
    test_cases = [
        (("5", 1, 10), True, "Value within range"),
        (("0", 1, 10), False, "Value below range"),
        (("11", 1, 10), False, "Value above range"),
        (("1", 1, 10), True, "Value at lower boundary"),
        (("10", 1, 10), True, "Value at upper boundary"),
        (("abc", 1, 10), False, "Non-numeric value"),
    ]
    for args, expected, desc in test_cases:
        got = ensure_return(techniques.range_check(*args), func_name)
        report(func_name, desc, got, expected)
        if got != expected:
            return False
    return True

test_list.append(test_range_check)

# Format check
def test_format_check():
    func_name = "format_check"
    test_cases = [
        (("25/12/2020",), True, "Valid date format"),
        (("01/01/1999",), True, "Valid date format"),
        (("31-12-2020",), False, "Invalid date format with dashes"),
        (("2020/12/25",), False, "Invalid date format with year first"),
        (("12/25/2020",), False, "Invalid date format with month first"),
        (("25/12/20",), False, "Invalid date format with two-digit year"),
        (("25/12",), False, "Incomplete date"),
        (("25/12/2020/extra",), False, "Extra data in date"),
    ]
    for args, expected, desc in test_cases:
        got = ensure_return(techniques.format_check(*args), func_name)
        report(func_name, desc, got, expected)
        if got != expected:
            return False
    return True

test_list.append(test_format_check)

# Length check
def test_length_check():
    func_name = "length_check"
    test_cases = [
        (("hello", 5), True, "Correct length"),
        (("hello", 4), False, "Too short"),
        (("hello", 6), False, "Too long"),
        (("", 0), True, "Empty string with zero length"),
        (("a", 1), True, "Single character string"),
    ]
    for args, expected, desc in test_cases:
        got = ensure_return(techniques.length_check(*args), func_name)
        report(func_name, desc, got, expected)
        if got != expected:
            return False
    return True

test_list.append(test_length_check)

#   Presence check
def test_presence_check():
    func_name = "presence_check"
    test_cases = [
        (("hello",), True, "Non-empty string"),
        (("",), False, "Empty string"),
        ((" ",), True, "String with space"),
    ]
    for args, expected, desc in test_cases:
        got = ensure_return(techniques.presence_check(*args), func_name)
        report(func_name, desc, got, expected)
        if got != expected:
            return False
    return True

test_list.append(test_presence_check)

#   Existence check
def test_existence_check():
    func_name = "existence_check"
    predefined_list = ["apple", "banana", "cherry"]
    test_cases = [
        (("apple", predefined_list), True, "Value exists in list"),
        (("date", predefined_list), False, "Value does not exist in list"),
        (("", predefined_list), False, "Empty string does not exist in list"),
        (("cherry", []), False, "Empty list does not contain value"),
    ]
    for args, expected, desc in test_cases:
        got = ensure_return(techniques.existence_check(*args), func_name)
        report(func_name, desc, got, expected)
        if got != expected:
            return False
    return True

test_list.append(test_existence_check)

#   Limit check

def test_limit_check():
    func_name = "limit_check"
    test_cases = [
        (("50", 100), True, "Value below limit"),
        (("100", 100), True, "Value at limit"),
        (("150", 100), False, "Value above limit"),
        (("abc", 100), False, "Non-numeric value"),
    ]
    for args, expected, desc in test_cases:
        got = ensure_return(techniques.limit_check(*args), func_name)
        report(func_name, desc, got, expected)
        if got != expected:
            return False
    return True

test_list.append(test_limit_check)

# Check digit
# This function verifies a number using a simple check digit algorithm:
# The last digit is the sum of all previous digits modulo 10.
# It should take one parameter: number.
def test_check_digit():
    func_name = "check_digit"
    test_cases = [
        (("12340",), True, "Valid check digit"),
        (("12344",), False, "Invalid check digit"),
        (("00000",), True, "All zeros with valid check digit"),
        (("00001",), False, "All zeros with invalid check digit"),
        (("5",), False, "Single digit number"),
        (("12a34",), False, "Non-numeric input"),
    ]
    for args, expected, desc in test_cases:
        got = ensure_return(techniques.check_digit(*args), func_name)
        report(func_name, desc, got, expected)
        if got != expected:
            return False
    return True

test_list.append(test_check_digit)

#   Parity check

def test_parity_check():
    func_name = "parity_check"
    test_cases = [
        (("1100",), True, "Even number of 1's"),
        (("1010",), True, "Even number of 1's"),
        (("1110",), False, "Odd number of 1's"),
        (("0000",), True, "No 1's"),
        (("1",), False, "Single 1"),
        (("0",), True, "Single 0"),
        (("1020",), False, "Invalid binary string"),
    ]
    for args, expected, desc in test_cases:
        got = ensure_return(techniques.parity_check(*args), func_name)
        report(func_name, desc, got, expected)
        if got != expected:
            return False
    return True

test_list.append(test_parity_check)

#   Checksum

def test_checksum():
    func_name = "checksum"
    test_cases = [
        (("ABC", 198), True, "Valid checksum"),
        (("ABC", 199), False, "Invalid checksum"),
        (("", 0), True, "Empty string with zero checksum"),
        (("A", 65), True, "Single character string"),
        (("156", 156), True, "Numeric string"),
        (("156", 157), False, "Numeric string with invalid checksum"),
    ]
    for args, expected, desc in test_cases:
        got = ensure_return(techniques.checksum(*args), func_name)
        report(func_name, desc, got, expected)
        if got != expected:
            return False
    return True

test_list.append(test_checksum)

#   Double entry
def test_double_entry():
    func_name = "double_entry"
    test_cases = [
        (("data", "data"), True, "Matching entries"),
        (("data", "Data"), False, "Non-matching entries (case sensitive)"),
        (("12345", "12345"), True, "Matching numeric entries"),
        (("12345", "12346"), False, "Non-matching numeric entries"),
    ]
    for args, expected, desc in test_cases:
        got = ensure_return(techniques.double_entry(*args), func_name)
        report(func_name, desc, got, expected)
        if got != expected:
            return False
    return True

test_list.append(test_double_entry)

# Optionally run all tests when this script is executed directly
if __name__ == "__main__":
    failed_tests = []
    for test_func in test_list:
        notify_test_start(test_func)
        try:
            if test_func():
                notify_test_success(test_func)
            else:
                failed_tests.append(test_func.__name__)
        except NotImplementedYet as e:
            failed_tests.append(test_func.__name__)
            print(e)
            break
    if failed_tests:
        print("\n -> Some tests failed:", failed_tests, "\nDon't give up, keep trying!")
    else:
        print("All tests passed successfully! ",
        "Congratulations on finishing the assignment. \n",
        "You may now submit your work.")
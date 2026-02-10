################################################################
# techniques.py
# This module contains various techniques related to data integrity,
# verification, and validation.
# Fill in the implementation details as needed.
# You may create additional helper functions if you want.
# Covered techniques:
#   Range check
#   Format check
#   Length check
#   Presence check
#   Existence check
#   Limit check
#   Check digit
#   Parity check
#   Checksum
#   Double entry
################################################################

# Range check
# This function checks if a value is within a specified range.
# It should take three parameters: value, min_value, and max_value.
def range_check(value: str, min_value: int, max_value :int) -> bool:
    pass  # Implement the range check logic here

# Format check
# This function checks if a value matches a specified date format.
# It should take one parameter: value.
# Assume the format is 'DD/MM/YYYY'.
def format_check(value: str) -> bool:
    pass  # Implement the format check logic here

# Length check
# This function checks if the length of a value is equal to a specified length.
# It should take two parameters: value and expected_length.
def length_check(value: str, expected_length: int) -> bool:
    pass  # Implement the length check logic here

# Presence check
# This function checks if a value is not empty.
# It should take one parameter: value.
def presence_check(value: str) -> bool:
    pass  # Implement the presence check logic here

# Existence check
# This function checks that value exists in a predefined list or database.
# It should take two parameters: value and list.
def existence_check(value: str, lst: list) -> bool:
    pass  # Implement the existence check logic here

# Limit check
# This function checks if a value does not exceed a specified limit.
# It should take two parameters: value and limit.
def limit_check(value: str, limit: int) -> bool:
    pass  # Implement the limit check logic here

# Check digit
# This function verifies a number using a simple check digit algorithm:
# The last digit is the sum of all previous digits modulo 10.
# It should take one parameter: number.
def check_digit(number: str) -> bool:
    pass  # Implement the check digit logic here

# Parity check
# This function checks if the number of 1's in a binary string is even.
# It should take one parameter: binary_string.
def parity_check(binary_string: str) -> bool:
    pass  # Implement the parity check logic here

# Checksum
# This function calculates a simple checksum by summing the ASCII values
# of all characters in a string and taking modulo 256.
# It should take two parameters: value and check_value.
def checksum(value: str, check_value: int) -> bool:
    pass  # Implement the checksum logic here

# Double entry
# This function checks if two entries match.
def double_entry(entry1: str, entry2: str) -> bool:
    pass  # Implement the double entry logic here
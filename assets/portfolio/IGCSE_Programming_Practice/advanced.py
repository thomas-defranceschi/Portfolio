##########################################
# write a function that takes the width of
# a tree and prints out a simple ASCII art
# representation of a tree with that width.
#
# For example, if the width is 5, the output
# should look like this:
#    *
#   ***
#  *****
#    |
##########################################


def print_tree(width: int) -> None:
    for i in range(width):
        if i % 2 == 0:
            spaces = " " * ((width - 1 - i) // 2)
            print(spaces + "*" * (i + 1))
    print(" " * ((width - 1) // 2) + "|")


# print_tree(25)


##########################################
# Write a function that takes an integer
# n and returns the total number of digits
# used to write all the numbers from 0 to n.
#
# For example, if n is 13, the numbers from
# 0 to 13 are: 0, 1, 2, 3, 4, 5, 6, 7,
# 8, 9, 10, 11, 12, 13. The total number
# of digits used is 18.
##########################################


def digit_count(number: int) -> int:
    count = 0

    for i in range(number + 1):
        count += len(str(i))

    return count


# print(digit_count(1000000))

#########################################
# Wrtite a function that takes a list of
# integers and returns a new list containing
# the square of the even numbers from the
# original list
#########################################

inputs = [8, 7, 23, 53, 0, 95, 64, 1, 8, 4, 44, 236]

def even_squares(numbers: list[int]) -> list[int]:
    new_list = []
    for i in numbers:
        if i % 2 == 0:
            new_list.append(i * i)
    return new_list


#print(even_squares(inputs))


#########################################
# Write a function that takes a list of
# integer and returns a new list with 
# the same values but
# with all duplicate values removed
#########################################

def without_dups(numbers : list[int]) -> list[int]:
    new_list = []
    for i in numbers:
        if not i in new_list:
            new_list.append(i)
    return new_list

# print(without_dups([1,1,1,0,0,5,6,5,9,9,5,9,6,0,0,1,5,9]))



#########################################
# Write a function that takes a list of
# integer and returns a new same list 
# with the same values but
# in ascending order
#########################################

test_list = [-1, 8, 5, 3, 4, 15, 0, 10, -85, 5]

def ascend(nums: list[int]) -> list[int]:
    outlist = []
    while len(nums) > 0:
        smallest = nums[0]
        for num in nums:
            if num < smallest:
                smallest = num
        outlist.append(smallest)
        nums.remove(smallest)
    return outlist

#print(ascend(test_list))

def bubble_sort(nums : list[int]) -> list[int]:
    is_sorted = False
    while not is_sorted:
        is_sorted = True
        for i in range(len(nums)-1):
            if nums[i] > nums[i+1]:
                tmp = nums[i]
                nums[i] = nums[i+1]
                nums[i+1] = tmp
                is_sorted = False
    return nums

print(bubble_sort(test_list))
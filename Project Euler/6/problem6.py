# Title: Sum square difference
# Problem Statement:
#
# The sum of the squares of the first ten natural numbers is,
# 1^2 + 2^2 + ... + 10^2 = 385
# 
# The square of the sum of the first ten natural numbers is,
# (1 + 2 + ... + 10)^2 = 55^2 = 3025
#
# Hence the difference between the sum of the squares of the first ten natural numbers and The
# square of the sum is 3025 - 385 = 2640.
#
# Find the difference between the sum of the squares of the first one hundred natural numbers and
# the square of the sum.

def sum_of_squares():
	result = 0
	for i in range(1, 101):
		result += i**2
	return result

def square_of_sums():
	result = 0
	for i in range(1, 101):
		result += i
	result = result**2
	return result

print (square_of_sums() - sum_of_squares())
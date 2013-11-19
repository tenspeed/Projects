# Title: Largest product in a series
# Problem Statement:
#
# Find the greatest product of five consecutive digits in the 1000-digit number given.

with open("number.txt") as f:
	data = f.read()

num_list = data.split('\n')

num = ''.join(num_list)

num_digits = 5
num_length = len(num)
largest_product = 0

for i in range(num_length - 4):
	digits = num[i:i+num_digits]
	product = (int(digits[0])*int(digits[1])*int(digits[2])*int(digits[3])*int(digits[4]))
	if product > largest_product:
		largest_product = product
		
print largest_product
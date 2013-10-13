# Title: Largest palindrome product
# Problem Statement:
# 
# A palindromic number reads the same both ways. The largest palindrome made from
# the product of two 2-digit numbers is 9009 = 91 X 99.
#
# Find the largest palindrome made from the product of two 3-digit numbers.

def flip(num):
	snum = str(num)
	return int(snum[::-1])

biggest = [0, 0, 0]

for i in range(100, 999):
	num1 = i
	for j in range(100, 999):
		num2 = j
		product = num1 * num2
		reverse = flip(product)
		if reverse == product:
			if product > biggest[2]:
				biggest[0] = num1
				biggest[1] = num2
				biggest[2] = product
		else:
			pass
print biggest
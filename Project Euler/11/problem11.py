# Title: Largest product in a grid
# Problem Statement:
#
# For a given 20x20 grid of integers, what is the greatest product of four adjacent numbers
# in the same direction (up, down, left, right, or diagonally)

with open("number_matrix.txt") as f:
	data = f.read()

num_list = data.split("\n")
temp_list = []
num_list_2D = [[[None] for i in range(20)] for i in range(20)]
product = 0
largest_product = 0

for i in range(len(num_list)):
	temp_list = num_list[i].split(" ")
	for j in range(len(temp_list)):
		num_list_2D[i][j] = int(temp_list[j])

for m in range(len(num_list_2D)):
	for n in range(len(num_list_2D)):	
		
		print "m: %d" % m
		print "n: %d" % n

		if (m >= len(num_list_2D) - 3):
			pass
		else:
			if (n < 3):
				product = num_list_2D[m][n]*num_list_2D[m+1][n+1]*num_list_2D[m+2][n+2]*num_list_2D[m+3][n+3]
				print "product dr: %d" % product
				if product > largest_product:
					largest_product = product
			elif (n > (len(num_list_2D) - 4)):
				product = num_list_2D[m][n]*num_list_2D[m-1][n-1]*num_list_2D[m-2][n-2]*num_list_2D[m-3][n-3]
				print "product dl: %d" % product
				if product > largest_product:
					largest_product = product
			else:
				product = num_list_2D[m][n]*num_list_2D[m+1][n+1]*num_list_2D[m+2][n+2]*num_list_2D[m+3][n+3]
				print "product drl: %d" % product
				if product > largest_product:
					largest_product = product

				product = num_list_2D[m][n]*num_list_2D[m-1][n-1]*num_list_2D[m-2][n-2]*num_list_2D[m-3][n-3]
				print "product dlr: %d" % product
				if product > largest_product:
					largest_product = product

		if n <= (len(num_list_2D) - 4):
			product = num_list_2D[m][n]*num_list_2D[m][n+1]*num_list_2D[m][n+2]*num_list_2D[m][n+3]
			print "product r: %d" % product
			if product > largest_product:
				largest_product = product
		else:
			pass
		if m <= (len(num_list_2D) - 4):
			product = num_list_2D[m][n]*num_list_2D[m+1][n]*num_list_2D[m+2][n]*num_list_2D[m+3][n]
			print "product c: %d" % product
			if product > largest_product:
				largest_product = product
		else:
			pass

		raw_input("> ")
print "largest product: %d" % largest_product
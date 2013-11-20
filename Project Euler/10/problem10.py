# Title: Summation of primes
# Problem Statement:
#
# The sum of the primes below 10 is 2 + 3 + 5 + 9 = 17.
#
# Find the sum of all the primes below two million.

primes = []

for i in range(2, 2000001):
	primes.append(i)

p_index =  0
p = primes[p_index]

while p != primes[-1]:
	index_shift = 0
	p = primes[p_index]
	print "p: %d" % p
	print "last num: %d" % primes[-1]

	for j in range(len(primes)):
		if primes[j - index_shift] == p:
			pass
		elif primes[j - index_shift] % p == 0:
			primes.pop(j - index_shift)
			index_shift += 1

	p_index += 1

p_sum = 0

for i in range(len(primes)):
	p_sum += primes[i]

print "number of primes found: %d" % len(primes)
print "sum of all primes found: %d" % p_sum
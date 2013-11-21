def is_prime(num, primes_list):
	for i in range(len(primes_list)):
		if num % primes_list[i] == 0:
			return False
		else:
			if i == (len(primes_list) - 1):
				return True

def get_primes(num, primes_list):
	while True:
		if is_prime(num, primes_list):
			primes_list.append(num)
			return primes_list
		else:
			num += 1

primes = [2, 3, 5, 7]
p_sum = 0

while primes[-1] <= 2000000:
	primes = get_primes(primes[-1] + 1, primes)
	print "number of primes found: %d" % len(primes)

primes.pop(-1)

for i in range(len(primes)):
	p_sum += primes[i]

print primes
print "\n"*2
print "number of primes: %d" % len(primes)
print "sum of all primes: %d" % p_sum
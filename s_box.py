# The Rijndael Sbox


# x and y are nonnegative integers 
# Their associated binary polynomials are multiplied. 
# The associated integer to this product is returned. 
def multiply_ints_as_polynomials(x, y):
	z = 0
	while x != 0:
		if x & 1 == 1:
			z ^= y
		y <<= 1
		x >>= 1
	return z


# Returns the number of bits that are used 
# to store the non-negative integer x.
def number_bits(x):
	nb = 0
	while x != 0:
		nb += 1
		x >>= 1
	return nb


# x is a nonnegative integer
# m is a positive integer
def mod_int_as_polynomial(x, m):
	nbm = number_bits(m)
	while True:
		nbx = number_bits(x) 
		if nbx < nbm:
			return x
		mshift = m << (nbx - nbm)
		x ^= mshift


# x,y are 8-bits
# The output value is 8-bits
def rijndael_multiplication(x, y):
	z = multiply_ints_as_polynomials(x, y)
	m = int('100011011', 2)
	return mod_int_as_polynomial(z, m)


# x is 8-bits
# The output value is 8-bits
# Here we find the inverse just through a brute force search.
def rijndael_inverse(x):
	if x == 0:
		return 0
	for y in range(1, 256):
		if rijndael_multiplication(x, y) == 1:
			return y


# x, y are nonnegative integers 
# considered as vectors of bits
def dot_product(x, y):
	z = x & y
	dot = 0  
	while z != 0:
		dot ^= z & 1
		z >>= 1
	return dot 


# A is a 64-bit integer that represents a
# 8 by 8 matrix of 0's and 1's
# x and b are 8-bit integers, considered as column vectors
# This function calculates A * x + b
def affine_transformation(A, x, b):
	y = 0
	for i in reversed(range(8)):
		row = (A >> 8 * i) & 0xff 
		bit = dot_product(row, x)
		y ^= (bit << i)
	return y ^ b


# The input value x and the output value
# of the function are both 8-bit integers
def rijndael_sbox(x):
	xinv = rijndael_inverse(x)
	A = int('1111100001111100001111100001111110001111110001111110001111110001', 2)
	b = int('01100011', 2)
	return affine_transformation(A, xinv, b)

# The input value x and the output value
# of the function are both 8-bit integers
def rijndael_inv_sbox(x):
  """
    Inputs: x a non negative integer
    Outputs: the rijndael s-box A*i(x)+b

    Remark. A is fixed 
  """
  A = int('0101001000101001100101000100101000100100100110110100000010100101', 2)
  b = int('00000101', 2)
  return rijndael_inverse(affine_transformation(A, x, b))


# Print the Rijndael S-Box as a table of 16 rows, 
# with 16 values per row (total of 256 values)
# if inverse=False prints the forward s-box
# else it prints the inverse s-box
def print_rijndael_sbox(inverse):
  if inverse==False:
    for row in range(16):
      for col in range(16):
        x = 16 * row + col
        hexstring = format(rijndael_sbox(x), "02x")
        print(hexstring, end=' ')
      print()	
  elif inverse==True:
    for row in range(16):
      for col in range(16):
        x = 16 * row + col
        hexstring = format(rijndael_inv_sbox(x), "02x")
        print(hexstring, end=' ')
      print()
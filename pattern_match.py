import random
import math

#To generate random prime less than N
def randPrime(N):
	primes = []
	for q in range(2,N+1):
		if(isPrime(q)):
			primes.append(q)
	return primes[random.randint(0,len(primes)-1)]

# To check if a number is prime
def isPrime(q):
	if(q > 1):
		for i in range(2, int(math.sqrt(q)) + 1):
			if (q % i == 0):
				return False
		return True
	else:
		return False

#pattern matching
def randPatternMatch(eps,p,x):
	N = findN(eps,len(p))
	q = randPrime(N)
	return modPatternMatch(q,p,x)

#pattern matching with wildcard
def randPatternMatchWildcard(eps,p,x):
	N = findN(eps,len(p))
	q = randPrime(N)
	return modPatternMatchWildcard(q,p,x)

# return appropriate N that satisfies the error bounds
def findN(eps,m):
    # using two inequalities
    # (1) ((eps)/m) >= log(26)/pi(N) and pi(N) >= N/(2*log(N))
	return int(((4*m)/eps)*(math.log(26,2))*(math.log((((2*m)/eps)*(math.log(26,2))),2)))





def pow(n,x):
    m=1
    for i in range(x):
        m = m*n
    return m


def modPatternMatch(q,p,x):
    # m = len(p)
    found_pattern=[] #this list stores the indices at which pattern is found in x
    
    w=pow(26,len(p)-1) % q #SPACE COMPLEXITY = O(log(q)) #storing the value of 26^(pattern_lenght-1) % q #Time complexity = O(m)
    # Now as hinted in assignment , we follow a hash function to convert a string to a unique integer :
    # (1) pattern_value correspondind to pattern p (2)current_value corresponding to the substring being checked in x
    pattern_value=0  
    current_value=0
#Now to optimise space complexity we divide pattern_value by q
#Also to optimise time complexity from O(mn) to O(q) as mentioned in assignment , instead of calculating the current_value by
#running loop over next pattern_lenght elements , we will subtract the (highest significant quantity)*26^(m-1) and multiply
#current value by 26 , then add the updated least significant quantity
   
    for i in range(len(p)): # Time complexity = O(m*log(q)) # assumed : basic arithmetic operation on 'p' bit is O(p) and we are doing this operation m times
        pattern_value = ((((26 % q)*pattern_value) % q) + ((ord(p[i])-65) % q)) % q #SPACE COMPLEXITY = O(log(q))
        current_value = ((((26 % q)*current_value) % q) + ((ord(x[i])-65) % q)) % q #SPACE COMPLEXITY = O(log(q))
# we will compare the values, and store only if current_value=pattern_value
    if (current_value) == pattern_value :
        found_pattern.append(0)

    for k in range(1,len(x)-len(p)+1): # Time complexity = O(n*log(q)) # assumed : basic arithmetic operation on 'p' bit is O(p) and we are doing this operation n times
        current_value = ((((current_value - ((((ord(x[k-1])-65) % q)*w) % q))*(26 % q)) % q)+ ((ord(x[k+len(p)-1])-65) % q)) % q #SPACE COMPLEXITY = O(log(q))
        if (current_value) == pattern_value:
            found_pattern.append(k)
    
    return found_pattern
#TOTAL SPACE COMPLEXITY USED IN modPatternMatch(q,p,x) FUNCTION:
# w : O(log(q))
# pattern_value : O(log(q))
# current_value : O(log(q))
# found_value : k
# for loop variable : O(log(n))
#Total space complexity = o(log(q)+log(n)+k)
#TOTAL TIME COMPLEXITY = O(n*log(q)+m*log(q)+m) = O((m+n)*log(q))


#To deal with '?' we have fixed the alphabet 'A' in place of '?' in the pattern  and also stored the position/index of '?' in pattern in variable wild_index
#and while checking the corresponding substrng in text starting at say index 'k' of text , we treat the alphabet x[k+wild_index] as alphabet 'A' irrespective of what it is originally
#in this way our bijective hash function works correctly
def modPatternMatchWildcard(q,p,x):
    # m = len(p)
    found_pattern=[] #this list stores the indices at which pattern is found in x
    w=pow(26,len(p)-1) % q #SPACE COMPLEXITY = O(log(q)) #storing the value of 26^(pattern_lenght-1) % q #Time complexity = O(m)
    # Now as hinted in assignment , we follow a hash function to convert a string to a unique integer :
    # (1) pattern_value correspondind to pattern p (2)current_value corresponding to the substring being checked in x
    pattern_value=0  
    current_value=0
    wild_index=0 #this contain the position index of '?' in pattern
#Now to optimise space complexity we divide pattern_value by q
#Also to optimise time complexity from O(mn) to O(q) as mentioned in assignment , instead of calculating the current_value by
#running loop over next pattern_lenght elements , we will subtract the (highest significant quantity)*26^(m-1) and multiply
#current value by 26 , then add the updated least significant quantity
    for i in range(len(p)): # Time complexity = O(m*log(q)) # assumed : basic arithmetic operation on 'p' bit is O(p) and we are doing this operation m times
        if p[i]!='?':
            pattern_value = ((((26 % q)*pattern_value) % q) + ((ord(p[i])-65) % q)) % q #SPACE COMPLEXITY = O(log(q))
            current_value = ((((26 % q)*current_value) % q) + ((ord(x[i])-65) % q)) % q #SPACE COMPLEXITY = O(log(q))
        else:
            pattern_value = ((((26 % q)*pattern_value) % q) + ((ord('A')-65) % q)) % q #SPACE COMPLEXITY = O(log(q))
            current_value = ((((26 % q)*current_value) % q) + ((ord('A')-65) % q)) % q #SPACE COMPLEXITY = O(log(q))
            wild_index=i

    s1=pow(26,len(p)-wild_index-1) % q #SPACE COMPLEXITY = O(log(q))
    s2=pow(26,len(p)-wild_index-2) % q #SPACE COMPLEXITY = O(log(q))


    
    if (current_value) == pattern_value :
        found_pattern.append(0)

    for k in range(1,len(x)-len(p)+1): # Time complexity = O(n*log(q)) # assumed : basic arithmetic operation on 'p' bit is O(p) and we are doing this operation n times
        if (wild_index != 0) and (wild_index != len(p)-1):
            current_value = (((((current_value - ((((ord(x[k-1])-65) % q)*w) % q) - ((((ord(x[k + wild_index])-65) % q)*s2) % q)+((((ord(x[k + wild_index-1])-65) % q)*s1) % q)) % q)*(26 % q)) % q) + ((ord(x[k+len(p)-1])-65) % q)) % q #SPACE COMPLEXITY = O(log(q))
            if (current_value) == pattern_value:
                found_pattern.append(k)

        elif wild_index == 0:
            current_value = ((((current_value  - ((((ord(x[k])-65) % q)*s2) % q) )*(26 % q)) % q) + ((ord(x[k+len(p)-1])-65) % q)) % q #SPACE COMPLEXITY = O(log(q))
            if (current_value) == pattern_value:
                found_pattern.append(k)
        elif wild_index == len(p)-1:
            current_value = ((((current_value - ((((ord(x[k-1])-65) % q)*w) % q))*(26 % q)) % q)+ ((((ord(x[k+len(p)-2])-65) % q)*(26 % q)) % q)) % q #SPACE COMPLEXITY = O(log(q))
            if (current_value) == pattern_value:
                found_pattern.append(k)

            
    
    return found_pattern
# TOTAL SPACE COMPLEXITY IN modPatternMatchWildcard(q,p,x):
# w : O(log(q))
# s1 : O(log(q))
# s2 : O(log(q))
# pattern_value : O(log(q))
# current_value : O(log(q))
# found_value : k
# for loop variable : O(log(n))
# Total space complexity = O(log(q))+O(log(n))+O(k) = O(log(q)+log(n)+O(k))
#TOTAL TIME COMPLEXITY = O(n*log(q)+m*log(q)+m) = O((m+n)*log(q))

print(findN(0.1,10))
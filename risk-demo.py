# A B and C are vault tokens, in dollar value.
# For better understanding, I suggest thinking in terms of USD, and not actual token amounts
# After all, this is what matters for users.
# Weights are equal (1/3)

A = 1
B = 100000
C = 100000

# S is total supply of index tokens in circulation
S = 1000

# input calculates the amount of index tokens you recieve by providing input_value tokens in token A.
# need to manually update S and basket after invoked
def input(input_value, token="A"):
    frac = 0
    if token == "A":
        frac = input_value / A + 1
    if token == "B":
        frac = input_value / B + 1
    if token == "C":
        frac = input_value / C + 1
    
    frac = frac ** (1/3) - 1
    indexOut = frac * S
    return indexOut

# out calculates the amount of token A, B, or C you recieve by providing outAmount index tokens.
# need to manually update S and basket after invoked
def out(outAmount, token="A"):
    par = 1 - outAmount / S
    bal = 0
    w = 1/3
    if token == "A":
        bal = A
    if token == "B":
        bal = B
    if token == "C":
        bal = C
        
    res = bal - bal * (par ** (1/w))
    return res

def allOut(outAmount):
    global A, B, C
    sum = 0
    prop = outAmount / S
    
    sum += A * prop
    A = A - A * prop
    sum += B * prop
    B = B - B * prop
    sum += C * prop
    C = C - C * prop
    return sum

def indexTokenValue():
    return (A + B + C) / S


def stats():
    print("Stats:")
    print("\tA: $" + str(A))
    print("\tB: $" + str(B))
    print("\tC: $" + str(C))
    print("\tS: " + str(S) + " with a single token worth $" + str(indexTokenValue()))
    print()

stats()

# Save the price of initial index token
initialIndexValue = indexTokenValue() 

depeggedIn = 99999 # The amount of tokens to mint in step 1
depeggedOut = input(depeggedIn, "A") # user receives index tokens

# update S and A
S += depeggedOut
A += depeggedIn

print("Performing all-token exit after joining the pool with $" + str(depeggedIn), "worth of token A.")
earnedValue = allOut(depeggedOut)
S -= depeggedOut

print("Earned Value: $", earnedValue)
print()
stats()

print("The index token has dropped in value by", str(1 - indexTokenValue() / initialIndexValue) + "%", "since the adversary joined the pool.")

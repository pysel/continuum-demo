# A B and C are vault tokens, in dollar value.
# For better understanding, I suggest thinking in terms of USD, and not actual token amounts
# After all, this is what matters to users.
# Weights are equal (1/3)
A = 100
B = 100
C = 100

# S is total supply of index tokens in circulation
S = 100

# input calculates the amount of index tokens you recieve by providing input_value tokens in token `token`.
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

# out calculates the amount of token A, B, or C you receive by providing outAmount index tokens.
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

# This tests the profitability of a strategy that goes like this:
# 1. some user provides (for example) token A to a fully balanced pool. This unbalances the pool
# 2. an adversary provides a different token (for example B) to the pool, receives X index tokens, and then exits via token A
# 3. the adversary receives more dollar-wise value in return than they provided (not always though)

AIn = 5 # The amount of tokens to mint in step 1
goodOut = input(AIn, "A") # user receives index tokens

# update S and A
S += goodOut
A += AIn

BIn_Adversary = 3 # The amount of tokens an adversary uses to mint in step 2.
# BIn_Adversary must not be higher than AIn to earn profit in this scenario.
adversaryIndices = input(BIn_Adversary, "B")

# update parameters
S += adversaryIndices
B += BIn_Adversary

# adversary performs an exit via A token
outFromAdversary = out(adversaryIndices, "A")

# not updating any values because they are irrelevant at this point

# check what the adversary has earned
print()
print("Adversary Provided (Dollars):", BIn_Adversary)
print()
print("Received Before Fee: ", outFromAdversary)
print("Profit Without Fee: ", outFromAdversary - BIn_Adversary)

print()
outPostFee = outFromAdversary * (1 - (0.0015 + 0.0007))

print("Received After Fee:", outPostFee)
print("Profit With Fee: ", outPostFee - BIn_Adversary)
print()

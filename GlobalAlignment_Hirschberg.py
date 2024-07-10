# Pentagon03
# Find global alignment of 2 Sequence in linear space using Hirschberg's algorithm

# match, mismatch, gap score (penalty)
our_info = [1,-1,-1]
# match, mismatch, gap = our_info 

# Basically global alignment
# Note that there can be different alginments with same score
# get alginment of A and B in linear space
def get_alignment(A:str, B:str, info = our_info):
    # use below line to get info in the parameter
    match, mismatch, gap = info
    n, m = len(A), len(B)
    # B is empty, just make it all gap
    if m == 0:
        return (A,'-'*n) 
    
    # make A, B 1-based string for convenience
    # after this, A[1]: 1st character of A.
    A = '$' + A
    B = '$' + B
    
    # base case 1: A is one letter
    if n == 1: # n <= m
        # the best is to find whether there is a same character in B
        id = 1 # if there is none, just put it in front (can be changed)
        for i in range(1,m+1):
            if B[i] == A[1]:
                id = i
                break
        # make length m string
        alignmentA = ('-'*(id-1)) + A[1] + ('-'*(m-id))
        alignmentB = B[1:] # this is quite important. get rid of reference issue.
    
    # base case 2: B is one letter
    elif m == 1: # n <= m
        # the best is to find whether there is a same character in A
        id = 1 # if there is none, just put it in front (can be changed)
        for i in range(1,n+1):
            if A[i] == B[1]:
                id = i
                break
        # make length n string
        alignmentA = A[1:] # this is quite important. get rid of reference issue.
        alignmentB = ('-'*(id-1)) + B[1] + ('-'*(n-id))
    
    # Recursion Case: n > 1, m > 1
    else:
        # if this doesn't work for linear space, make it global variable
        # and then, just use it inside of get_alignment function
        
        # find middle node
        mid = (1+n)//2

        # dp1[2][m+1] -> dp from front 1 ~ mid
        dp1 = [[0]*(m+1) for _ in range(2)]

        # dp2[2][m+2] -> dp from end n ~ mid+1
        dp2 = [[0]*(m+2) for _ in range(2)]

        f1 = 0
        # [0,m]
        for j in range(m+1):
            dp1[f1][j] = gap * j
        # A[1,mid]
        for i in range(1,mid+1): 
            f1 = not f1
            dp1[f1][0] = gap * i
            # B[1,m]
            for j in range(1,m+1):
                dp1[f1][j] = max(
                    dp1[not f1][j] + gap, # A[i] and space
                    dp1[f1][j-1] + gap, # B[i] and space
                    dp1[not f1][j-1] + (match if A[i]==B[j] else mismatch) # A[i] and B[i]
                )
        f2 = 0
        # [m+1,1]
        for j in range(m+1,0,-1):
            dp2[f2][j] = gap * (m+1-j)
        # A[n,mid+1]
        for i in range(n,mid,-1):
            f2 = not f2
            dp2[f2][m+1] = gap * (n+1-i)
            # B[m:1]
            for j in range(m,0,-1):
                dp2[f2][j] = max(
                    dp2[not f2][j] + gap, # A[i] and space
                    dp2[f2][j+1] + gap, # B[i] and space 
                    dp2[not f2][j+1] + (match if A[i]==B[j] else mismatch)
                )
        # what's the best dividing point? = find the path node (mid,j)
        best = 0
        for j in range(1,m+1):
            if dp1[f1][j] + dp2[f2][j+1] > dp1[f1][best] + dp2[f2][best+1]:
                best = j
        # print(dp1[f1][best] + dp2[f2][best+1])
        # divide into 2 strings
        ans1 = get_alignment(A[1:mid+1],B[1:best+1],info)
        ans2 = get_alignment(A[mid+1:],B[best+1:],info)
        alignmentA = ans1[0] + ans2[0]
        alignmentB = ans1[1] + ans2[1]
    
    #all done
    return (alignmentA,alignmentB)

def find_score(alignmentA:str, alignmentB:str, info = our_info) -> int:
    match, mismatch, gap = info
    an, am = len(alignmentA), len(alignmentB)
    if an != am:
        print("This is not an alignment")
        return -999999999
    score = 0
    for i in range(an):
        if alignmentA[i] != '-' and alignmentB[i] != '-':
            score += match if alignmentA[i] == alignmentB[i] else mismatch
        else:
            score += gap
    return score
if __name__ == "__main__":
    # A = input()
    # B = input()
    A = "GCATGCG"
    B = "GATTACA"
    alignmentA, alignmentB = get_alignment(A,B,[1,-1,-1])
    print(alignmentA)
    print(alignmentB)
    diff = ""
    for i in range(len(alignmentA)):
        diff += "+" if alignmentA[i] == alignmentB[i] else "-"
    print(diff)
    print(f"Score:{find_score(alignmentA,alignmentB)}")

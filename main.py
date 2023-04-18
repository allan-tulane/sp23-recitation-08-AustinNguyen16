
####### Problem 3 #######

test_cases = [('book', 'back'), ('kookaburra', 'kookybird'), ('elephant', 'relevant'), ('AAAGAATTCA', 'AAATCA')]
alignments = [('book', 'back'), ('kookaburra', 'kookybird-'), ('relev-ant','-elephant'), ('AAAGAATTCA', 'AAA---T-CA')]

def MED(S, T):
    m, n = len(S), len(T)
    table = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                table[i][j] = j
            elif j == 0:
                table[i][j] = i 
            elif S[i-1] == T[j-1]:
                table[i][j] = table[i-1][j-1]
            else:
                table[i][j] = 1 + min(table[i][j-1], table[i-1][j], table[i-1][j-1])
    return table[m][n]

def fast_MED(S, T, MED={}):
    if (S, T) in MED:
        return MED[(S, T)]
    if (T, S) in MED:
        return MED[(T, S)]

    if (S == ""):
        result = len(T)
    elif (T == ""):
        result = len(S)
    elif (S[0] == T[0]):
        result = fast_MED(S[1:], T[1:], MED)
    else:
        result = 1 + min(fast_MED(S, T[1:], MED), 
                         fast_MED(S[1:], T, MED),  
                         fast_MED(S[1:], T[1:], MED))

    MED[(S, T)] = result
    return result

def fast_align_MED(S, T, MED={}):
    if (S == ""):
        return ('-' * len(T), T)
    elif (T == ""):
        return (S, '-' * len(S))
    elif (S[0] == T[0]):
        align_S, align_T = fast_align_MED(S[1:], T[1:], MED)
        return (S[0] + align_S, T[0] + align_T)
    else:
        replace = fast_MED(S[1:], T[1:], MED)
        insert = fast_MED(S, T[1:], MED)
        remove = fast_MED(S[1:], T, MED)

        min_val = min(replace, insert, remove)

        if min_val == replace:
            align_S, align_T = fast_align_MED(S[1:], T[1:], MED)
            return (S[0] + align_S, T[0] + align_T)
        elif min_val == insert:
            align_S, align_T = fast_align_MED(S, T[1:], MED)
            return ('-' + align_S, T[0] + align_T)
        else:
            align_S, align_T = fast_align_MED(S[1:], T, MED)
            return (S[0] + align_S, '-' + align_T)

def test_MED():
    for S, T in test_cases:
        assert fast_MED(S, T) == MED(S, T)
                                 
def test_align():
    for i in range(len(test_cases)):
        S, T = test_cases[i]
        align_S, align_T = fast_align_MED(S, T)
        assert (align_S == alignments[i][0] and align_T == alignments[i][1])

#for i in range(len(test_cases)):
 #       S, T = test_cases[i]
  #    print(align_S)
    #    print(alignments[i][0])
   #     print(align_T)
    #    print(alignments[i][1])
  #


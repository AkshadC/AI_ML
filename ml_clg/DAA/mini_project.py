def naive_string_match(pat, txt):
    m = len(pat)
    n = len(txt)

    for i in range(n - m + 1):
        j = 0

        while j < m:
            if txt[i + j] != pat[j]:
                break
            j += 1

        if j == m:
            print("Pattern found at index ", i)


def rabin_carp_string_match(pat, txt, q):
    d = 256
    m = len(pat)
    n = len(txt)
    j = 0
    p = 0
    t = 0
    h = 1

    for i in range(m - 1):
        h = (h * d) % q

    for i in range(m):
        p = (d * p + ord(pat[i])) % q
        t = (d * t + ord(txt[i])) % q

    for i in range(n - m + 1):

        if p == t:
            for j in range(m):
                if txt[i + j] != pat[j]:
                    break
                else:
                    j += 1
            if j == m:
                print("Pattern found at index " + str(i))

        if i < n - m:
            t = (d * (t - ord(txt[i]) * h) + ord(txt[i + m])) % q

            if t < 0:
                t = t + q


if __name__ == "__main__":
    txt = input("Enter the String: ")
    pat = input("Enter the string to search: ")
    q = 101

    # For naive working
    print("BY NAIVE METHOD")
    naive_string_match(pat, txt)

    # For rabin carp
    print("BY RABIN CARP METHOD")
    rabin_carp_string_match(pat, txt, q)

    ''' RABIN CARP VS NAIVE METHOD 
        Naive:
                Its time complexity is O(m(n-m+1)) in the worst case.
                There is no scope of improvement in it.
                Compares the pattern with the whole string for each bit.
                No extra computation required.
        Rabin Carp:
                Its time complexity is O(mn) in worst case but in best case its O(n-m+1).
                Algo can be improved more and more by taking better hash functions.
                The algo uses concept of hash value for string matching instead like naive (direct match).
                compute hash value for each subpattern again and again.
    '''

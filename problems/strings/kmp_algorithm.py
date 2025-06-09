def compute_lps_array(pattern):
    """
    Computes the Longest Proper Prefix which is also a Suffix (LPS) array
    for a given pattern.
    """
    m = len(pattern)
    lps = [0] * m  # Initialize LPS array with zeros
    length = 0     # Length of the previous longest prefix suffix
    i = 1          # Pointer to iterate through the pattern

    # The loop calculates lps[i] for i = 1 to m-1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            # This is tricky:
            # If there's a mismatch (pattern[i] != pattern[length])
            # and 'length' is not 0, we can use the LPS value of the
            # previous character in the prefix (lps[length-1]) to find
            # a shorter prefix that could match.
            if length != 0:
                length = lps[length - 1]
            else:
                # If length is 0, no common prefix-suffix found,
                # so lps[i] remains 0, and we just move to the next char in pattern
                lps[i] = 0
                i += 1
    return lps

def kmp_search(text, pattern):
    """
    Performs KMP string searching to find all occurrences of pattern in text.
    Returns a list of starting indices where the pattern is found.
    """
    n = len(text)
    m = len(pattern)

    if m == 0:
        return [i for i in range(n + 1)] # Empty pattern matches everywhere (before each char)
    if n == 0:
        return [] # Empty text has no matches

    lps = compute_lps_array(pattern)

    i = 0  # Pointer for text[] (index of text)
    j = 0  # Pointer for pattern[] (index of pattern)
    occurrences = [] # List to store starting indices of matches

    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == m:
            # Pattern found at index (i - j)
            occurrences.append(i - j)
            # After a match, use LPS array to prepare for next possible match
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            # Mismatch after j matches
            if j != 0:
                # Don't match lps[0..lps[j-1]-1] characters,
                # they will match anyway
                j = lps[j - 1]
            else:
                # If j is 0, just move to the next character in text
                i += 1
    return occurrences

"""
Given two strings needle and haystack, return the index of the first occurrence of needle in haystack, or -1 if needle is not part of haystack.



Example 1:

Input: haystack = "sadbutsad", needle = "sad"
Output: 0
Explanation: "sad" occurs at index 0 and 6.
The first occurrence is at index 0, so we return 0.
Example 2:

Input: haystack = "leetcode", needle = "leeto"
Output: -1
Explanation: "leeto" did not occur in "leetcode", so we return -1.


Constraints:

1 <= haystack.length, needle.length <= 104
haystack and needle consist of only lowercase English characters.
"""

def preprocess_string(needle: str)-> list[int]:
    n = len(needle)
    lps = [0] * n
    length = 0
    i = 1

    while i < n:
        if needle[length] == needle[i]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def strStr(haystack, needle) -> int:
    haystack_len = len(haystack)
    needle_len = len(needle)

    if needle_len == 0:
        return 0

    if haystack_len < needle_len:
        return -1

    i = j = 0
    lps = preprocess_string(needle)

    while i < haystack_len:
        if needle[j] == haystack[i]:
            i += 1
            j += 1

        if j == needle_len:
            return i - j
        elif i < haystack_len and needle[j] != haystack[i]:
            if j != 0:
                j = lps[j-1]
            else:
                i += 1

    return -1

import pytest

from problems.strings.leetcode_28 import strStr

# Assume the solution function is named `strStr` and is imported or defined here.
# For example, if you have a class Solution:
# class Solution:
#     def strStr(self, haystack: str, needle: str) -> int:
#         # Your KMP or built-in solution here
#         # Example simple implementation (not KMP):
#         if not needle:
#             return 0
#         if not haystack:
#             return -1
#
#         for i in range(len(haystack) - len(needle) + 1):
#             if haystack[i:i+len(needle)] == needle:
#                 return i
#         return -1


@pytest.mark.parametrize("haystack, needle, expected", [
    # --- Basic Cases ---
    ("sadbutsad", "sad", 0),  # Pattern at the beginning
    ("leetcode", "code", 4),  # Pattern in the middle
    ("hello", "ll", 2),      # Common case
    ("aaaaa", "bba", -1),    # No match
    ("mississippi", "issip", 4), # Overlapping pattern (should find first occurrence)

    # --- Edge Cases with Empty Strings ---
    ("", "", 0),              # Both empty: needle found at index 0
    ("abc", "", 0),           # Empty needle: always found at index 0
    ("", "abc", -1),          # Empty haystack, non-empty needle: not found

    # --- Boundary Cases for Lengths ---
    ("a", "a", 0),            # Single character match
    ("a", "b", -1),           # Single character no match
    ("ab", "b", 1),           # Needle at the end of a short haystack
    ("ab", "a", 0),           # Needle at the beginning of a short haystack
    ("abc", "abcd", -1),      # Needle longer than haystack

    # --- Cases involving repeated characters or patterns (relevant for KMP) ---
    ("aaaaa", "aaa", 0),      # Multiple overlapping matches, find first
    ("ababa", "aba", 0),      # Overlapping suffix/prefix
    ("ababa", "bab", 1),      # Overlapping match in middle
    ("abcabcabc", "abc", 0),  # Repeated pattern at start
    ("abcabcabc", "bca", 1),  # Repeated pattern inside

    # --- Cases where pattern is at the very end ---
    ("abcde", "de", 3),
    ("abcde", "e", 4),

    # --- Long Strings (performance check) ---
    # Note: For actual long strings, you might generate them dynamically or use pre-defined ones.
    # For a general test suite, these represent the concept.
    ("a" * 1000 + "b" + "a" * 1000, "b", 1000), # Needle in a very long haystack
    ("a" * 2000, "b", -1),                  # No match in very long haystack
    ("x" * 1000 + "y", "x" * 500, 0),         # Long overlapping needle

    # --- Specific KMP-related patterns (though not strictly required for a generic strStr) ---
    # These might expose issues if a naive algorithm is used and performance is critical,
    # or if a KMP implementation has flaws.
    ("aaaaaaaab", "aaab", 5), # Pattern with common prefix, KMP handles efficiently
    ("abxabcabcaby", "abcaby", 6), # A slightly more complex pattern
    ("abcxabcxabcxabcx", "abcxabcx", 0), # Complex repeated pattern
])
def test_str_str(haystack, needle, expected):
    """
    Test cases for LeetCode 28: Find the Index of the First Occurrence in a String.
    """
    # Assuming 'Solution' class and 'strStr' method
    result = strStr(haystack, needle)
    assert result == expected

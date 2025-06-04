# tests/test_rotate_string.py
# Import the function directly from your solution file
from problems.strings.rotate_string import rotateString

class TestRotateStringPytest: # No inheritance from unittest.TestCase needed

    # --- Comprehensive Test Cases for Rotate String Problem (Pytest Style) ---

    # 1. Basic Functionality Tests
    def test_basic_rotation_true_1(self):
        """s="abcde", goal="cdeab" -> True"""
        assert rotateString("abcde", "cdeab") is True

    def test_basic_rotation_true_2(self):
        """s="abcde", goal="eabcd" -> True"""
        assert rotateString("abcde", "eabcd") is True

    def test_basic_rotation_true_3(self):
        """s="hello", goal="llohe" -> True"""
        assert rotateString("hello", "llohe") is True

    def test_basic_rotation_false_1(self):
        """s="abcde", goal="abced" -> False (mismatched characters)"""
        assert rotateString("abcde", "abced") is False

    def test_basic_rotation_false_2(self):
        """s="world", goal="wodrl" -> False"""
        assert rotateString("world", "wodrl") is False

    # 2. Edge Cases: Empty Strings
    def test_both_empty_strings(self):
        """s="", goal="" -> True"""
        assert rotateString("", "") is True

    def test_s_empty_goal_not_empty(self):
        """s="", goal="a" -> False"""
        assert rotateString("", "a") is False

    def test_goal_empty_s_not_empty(self):
        """s="a", goal="" -> False"""
        assert rotateString("a", "") is False

    # 3. Edge Cases: Single Character Strings
    def test_single_char_match(self):
        """s="a", goal="a" -> True"""
        assert rotateString("a", "a") is True

    def test_single_char_mismatch(self):
        """s="a", goal="b" -> False"""
        assert rotateString("a", "b") is False

    # 4. Edge Cases: Different Lengths
    def test_s_longer_than_goal(self):
        """s="abcd", goal="abc" -> False"""
        assert rotateString("abcd", "abc") is False

    def test_s_shorter_than_goal(self):
        """s="abc", goal="abcd" -> False"""
        assert rotateString("abc", "abcd") is False

    # 5. Cases with Repeating Characters
    def test_repeating_chars_identical(self):
        """s="aaaaa", goal="aaaaa" -> True"""
        assert rotateString("aaaaa", "aaaaa") is True

    def test_repeating_chars_true_complex(self):
        """s="ababa", goal="baaba" -> True (multiple shifts needed)"""
        assert rotateString("ababa", "baaba") is True

    def test_repeating_chars_true_simple(self):
        """s="abab", goal="baba" -> True"""
        assert rotateString("abab", "baba") is True

    def test_repeating_chars_false_permutation(self):
        """s="abcabc", goal="abccba" -> False (is a permutation, but not a rotation)"""
        assert rotateString("abcabc", "abccba") is False

    def test_repeating_chars_true_misplaced(self):
        """s="aaaaab", goal="aaabaa" -> False"""
        assert rotateString("aaaaab", "aaabaa") is True

    # 6. Cases with Special Characters and Numbers
    def test_special_chars_true_1(self):
        """s="!@#$%", goal="#$%!@" -> True"""
        assert rotateString("!@#$%", "#$%!@") is True

    def test_special_chars_true_2(self):
        """s="12345", goal="34512" -> True"""
        assert rotateString("12345", "34512") is True

    def test_special_chars_true_3(self):
        """s="a-b_c", goal="b_ca-" -> True"""
        assert rotateString("a-b_c", "b_ca-") is True

    def test_special_chars_false_1(self):
        """s="!@#$%", goal="!@#$%^" -> False (different character)"""
        assert rotateString("!@#$%", "!@#$%^") is False

    def test_special_chars_false_2(self):
        """s="123", goal="124" -> False"""
        assert rotateString("123", "124") is False

    # 7. Long Strings
    def test_long_string_true(self):
        """Long strings that are rotatable."""
        long_s = "a" * 5000 + "b" + "c" * 5000
        long_goal = "c" * 5000 + "a" * 5000 + "b"
        assert rotateString(long_s, long_goal) is True

    def test_long_string_false(self):
        """Long strings that are not rotatable."""
        long_s = "a" * 5000 + "b" + "c" * 5000
        long_goal = "a" * 5000 + "d" + "c" * 5000 # Single character difference
        assert rotateString(long_s, long_goal) is False

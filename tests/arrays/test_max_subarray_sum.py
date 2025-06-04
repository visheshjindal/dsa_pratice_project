import pytest
from problems.arrays.max_subarray_sum import max_subarray_sum

class TestMaxSubarraySumPytest:

    # 1. Basic Cases
    @pytest.mark.parametrize("nums, expected_sum", [
        # Example 1: Classic Kadane's example with mixed numbers
        ([-2, 1, -3, 4, -1, 2, 1, -5, 4], 6), # Subarray: [4, -1, 2, 1]

        # Example 2: All positive numbers
        ([1, 2, 3, 4, 5], 15), # Subarray: [1, 2, 3, 4, 5]

        # Example 3: All negative numbers (result is the largest single negative number)
        ([-1, -2, -3, -4, -5], -1), # Subarray: [-1]
        ([-10, -5, -1, -8], -1), # Subarray: [-1]

        # Example 4: Mixed positive/negative, but starting with a peak
        ([5, -1, -2, 4, 3], 9), # Subarray: [5, -1, -2, 4, 3]

        # Example 5: Result is a single element
        ([2, -5, 7, -1, -2], 7), # Subarray: [7]
    ])
    def test_basic_cases(self, nums, expected_sum):
        assert max_subarray_sum(nums) == expected_sum

    # 2. Edge Cases

    def test_single_element_array(self):
        """Array with a single element (positive, negative, zero)"""
        assert max_subarray_sum([7]) == 7
        assert max_subarray_sum([-5]) == -5
        assert max_subarray_sum([0]) == 0

    def test_empty_array(self):
        """Empty array (assuming 0 as sum, as per problem definition)"""
        assert max_subarray_sum([]) == 0

    @pytest.mark.parametrize("nums, expected_sum", [
        # Zeros at ends
        ([0, 1, -2, 3, 0], 3), # Subarray: [3]
        ([-1, 0, 1], 1),
        ([1, 0, -1], 1),
        ([0, 0, 1, 0, 0], 1),

        # Zeros in the middle
        ([1, 0, 1, -2, 1], 2), # Subarray: [1, 0, 1]
        ([-2, 0, -1], 0), # Subarray: [0]
        ([1, -1, 0, 1], 1), # Subarray: [1] or [0,1]

        # All zeros
        ([0, 0, 0, 0], 0), # Subarray: [0] or [0,0,0,0]
    ])
    def test_arrays_with_zeros(self, nums, expected_sum):
        assert max_subarray_sum(nums) == expected_sum

    @pytest.mark.parametrize("nums, expected_sum", [
        # Cases where the optimal subarray spans across positive and negative
        ([10, -4, 3, 1, 5, 6, -35, 10, 20, -30], 30), # Subarray: [10, 20]
        ([1, -2, 3, -1, 2, 1, -5, 4], 5), # Subarray: [3, -1, 2, 1]
        ([-2, 1, -3, 4, -1, 2, 1, -5, 4], 6),
    ])
    def test_complex_mixed_arrays(self, nums, expected_sum):
        assert max_subarray_sum(nums) == expected_sum

    # Large Numbers (mainly for sanity check; Python integers handle arbitrary size)
    def test_large_numbers(self):
        large_nums = [10**9, -10**9, 2 * (10**9)] # Max sum should be 2 * 10^9
        assert max_subarray_sum(large_nums) == 2 * (10**9)

        large_nums_mixed = [-(10**9), 5 * (10**9), -(2 * 10**9), 3 * (10**9)]
        assert max_subarray_sum(large_nums_mixed) == 6 * (10**9) # 5*10^9 + 3*10^9 = 8*10^9, but it might be just 5*10^9 or 3*10^9. Let's trace it.
        # [-(10**9), 5 * (10**9), -(2 * 10**9), 3 * (10**9)]
        # current_max = max(nums[i], current_max + nums[i])
        # 1: -10^9
        # 2: max(5*10^9, -10^9 + 5*10^9) = 5*10^9 -> max_so_far = 5*10^9
        # 3: max(-2*10^9, 5*10^9 - 2*10^9) = 3*10^9 -> max_so_far = 5*10^9
        # 4: max(3*10^9, 3*10^9 + 3*10^9) = 6*10^9 -> max_so_far = 6*10^9
        assert max_subarray_sum(large_nums_mixed) == 6 * (10**9)

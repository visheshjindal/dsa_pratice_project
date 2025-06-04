def max_subarray_sum(A) -> int:
    """
        Finds the contiguous subarray within an array A that has the largest sum.

        Args:
            A: A list of integers (can contain positive, negative, and zero).

        Returns:
            The largest sum of a contiguous subarray.
    """
    if not A:
        return 0

    current_max = A[0]
    global_max = A[0]

    for i in range(1, len(A)):
        num = A[i]

        current_max = max(num, current_max + num)
        global_max = max(global_max, current_max)
    return global_max

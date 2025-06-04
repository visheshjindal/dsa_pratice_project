# Complexity O(N2)
def rotateString(s, goal) -> bool:
    """
        Brute-force solution for LeetCode 796: Rotate String.

        Checks if string 's' can be transformed into string 'goal' by
        trying every possible shift.

        Args:
            s: The original string.
            goal: The string to check if it's a rotation of 's'.

        Returns:
            True if 'goal' is a rotation of 's', False otherwise.
    """
    if len(s) != len(goal):
        return False

    if not s and not goal:
        return True

    n = len(s)
    for i in range(n):
        current_rotated_string = s[i:] + s[:i]

        if current_rotated_string == goal:
            return True
    return False

# Complexity O(N)
def optimal_rotate_string(s, goal):
    if len(s) != len(goal):
        return False

    if not s and not goal:
        return True

    return goal in (s+s)

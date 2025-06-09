# Checks if string 's' can be transformed into string 'goal' by trying every possible shift.
def preprocess_pattern(pattern: str) -> list[int]:
    n = len(pattern)
    lps = [0] * n
    length = 0
    i = 1

    while i < n:
        if pattern[i] == pattern[length]:
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

def rotateString(s, goal) -> bool:
    if len(s) != len(goal):
        return False

    if not s and not goal:
        return True

    concatenated_string = s + s
    processed_pattern = preprocess_pattern(goal)
    i = j = 0

    while i < len(concatenated_string):
        if goal[j] == concatenated_string[i]:
            i += 1
            j += 1

        if j == len(goal):
            return True
        elif i < len(concatenated_string) and goal[j] != concatenated_string[i]:
            if j != 0:
                j = processed_pattern[j - 1]
            else:
                i += 1

    return False

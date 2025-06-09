class RabinKarp:
    """
    Rabin-Karp String Matching Algorithm Implementation

    The Rabin-Karp algorithm uses rolling hash technique to find pattern(s)
    in a text efficiently. It's particularly powerful for multiple pattern searches.

    Key Concepts:
    1. Rolling Hash: Efficiently compute hash of sliding window in O(1) time
    2. Hash Collision: When two different strings have same hash value
    3. Spurious Hit: False positive when hashes match but strings don't
    """

    def __init__(self, base=256, prime=101):
        """
        Initialize Rabin-Karp with hash parameters

        Args:
            base (int): Base for polynomial rolling hash (typically 256 for ASCII)
            prime (int): Large prime number to reduce hash collisions
                        Common choices: 101, 1009, 10007, 1000000007

        Why these values?
        - Base 256: Covers all ASCII characters efficiently
        - Prime 101: Small enough to avoid overflow, large enough for good distribution
        """
        self.base = base
        self.prime = prime

    def compute_hash(self, string, length):
        """
        Compute polynomial rolling hash for a string

        Formula: hash = (s[0] * base^(n-1) + s[1] * base^(n-2) + ... + s[n-1]) % prime

        Args:
            string (str): Input string
            length (int): Length of substring to hash

        Returns:
            int: Hash value

        Time Complexity: O(length)
        Space Complexity: O(1)
        """
        hash_value = 0
        for i in range(length):
            # Polynomial hash: each character weighted by base^position
            hash_value = (hash_value * self.base + ord(string[i])) % self.prime
        return hash_value

        hash_value = 0
        for i in range(length):
            hash_value = (hash_value * self.base + ord(string[i])) % self.prime


    def recalculate_hash(self, old_hash, old_char, new_char, pattern_length):
        """
        Rolling hash calculation - the heart of Rabin-Karp efficiency

        Instead of recalculating entire hash, we:
        1. Remove contribution of outgoing character
        2. Add contribution of incoming character

        Formula: new_hash = (old_hash - old_char * base^(m-1)) * base + new_char

        Args:
            old_hash (int): Previous hash value
            old_char (str): Character being removed from window
            new_char (str): Character being added to window
            pattern_length (int): Size of sliding window

        Returns:
            int: New hash value

        Time Complexity: O(1) - This is the key optimization!
        """
        # Calculate base^(pattern_length-1) mod prime
        # This represents the weight of the leftmost character
        base_power = pow(self.base, pattern_length - 1, self.prime)

        # Remove old character's contribution
        # Subtract (old_char * base^(m-1)) and handle negative numbers
        new_hash = (old_hash - ord(old_char) * base_power) % self.prime

        # Shift left by multiplying with base and add new character
        new_hash = (new_hash * self.base + ord(new_char)) % self.prime

        # Ensure positive result (Python's % can return negative for negative inputs)
        if new_hash < 0:
            new_hash += self.prime

        return new_hash

    def search_single_pattern(self, text, pattern):
        """
        Find all occurrences of a single pattern in text

        Algorithm Steps:
        1. Calculate hash of pattern
        2. Calculate hash of first window in text
        3. Slide window through text, updating hash in O(1)
        4. When hashes match, verify character-by-character

        Args:
            text (str): Text to search in
            pattern (str): Pattern to find

        Returns:
            list: All starting indices where pattern is found

        Time Complexity: O(n + m) average, O(nm) worst case
        Space Complexity: O(1)
        """
        if not text or not pattern or len(pattern) > len(text):
            return []

        matches = []
        pattern_length = len(pattern)
        text_length = len(text)

        # Step 1: Calculate pattern hash
        pattern_hash = self.compute_hash(pattern, pattern_length)

        # Step 2: Calculate hash of first window in text
        text_hash = self.compute_hash(text, pattern_length)

        # Step 3: Check first window
        if pattern_hash == text_hash and text[:pattern_length] == pattern:
            matches.append(0)

        # Step 4: Slide the window and check each position
        for i in range(1, text_length - pattern_length + 1):
            # Rolling hash: remove leftmost char, add rightmost char
            text_hash = self.recalculate_hash(
                text_hash,
                text[i-1],  # Character leaving the window
                text[i + pattern_length - 1],  # Character entering the window
                pattern_length
            )

            # If hashes match, verify with actual string comparison
            # This handles hash collisions (spurious hits)
            if pattern_hash == text_hash:
                if text[i:i + pattern_length] == pattern:
                    matches.append(i)

        return matches

    def search_multiple_patterns(self, text, patterns):
        """
        Find all occurrences of multiple patterns in text

        This is where Rabin-Karp truly shines - we can search for
        multiple patterns simultaneously by maintaining multiple hashes

        Args:
            text (str): Text to search in
            patterns (list): List of patterns to find

        Returns:
            dict: Dictionary mapping pattern to list of indices

        Time Complexity: O(n * k + m * k) where k is number of patterns
        """
        if not text or not patterns:
            return {}

        results = {pattern: [] for pattern in patterns}

        # Group patterns by length for efficiency
        patterns_by_length = {}
        for pattern in patterns:
            length = len(pattern)
            if length not in patterns_by_length:
                patterns_by_length[length] = []
            patterns_by_length[length].append(pattern)

        # Search for each group of same-length patterns
        for pattern_length, pattern_group in patterns_by_length.items():
            if pattern_length > len(text):
                continue

            # Calculate hashes for all patterns of this length
            pattern_hashes = {}
            for pattern in pattern_group:
                pattern_hashes[self.compute_hash(pattern, pattern_length)] = pattern

            # Slide window through text
            text_hash = self.compute_hash(text, pattern_length)

            # Check first window
            if text_hash in pattern_hashes:
                candidate_pattern = pattern_hashes[text_hash]
                if text[:pattern_length] == candidate_pattern:
                    results[candidate_pattern].append(0)

            # Check remaining windows
            for i in range(1, len(text) - pattern_length + 1):
                text_hash = self.recalculate_hash(
                    text_hash,
                    text[i-1],
                    text[i + pattern_length - 1],
                    pattern_length
                )

                if text_hash in pattern_hashes:
                    candidate_pattern = pattern_hashes[text_hash]
                    if text[i:i + pattern_length] == candidate_pattern:
                        results[candidate_pattern].append(i)

        return results


def demonstrate_rabin_karp():
    """
    Comprehensive demonstration of Rabin-Karp algorithm capabilities
    """
    print("=== RABIN-KARP ALGORITHM DEMONSTRATION ===\n")

    # Initialize with different parameters for comparison
    rk_small = RabinKarp(base=256, prime=101)      # Good for small texts
    rk_large = RabinKarp(base=256, prime=1009)     # Better collision resistance

    # Test Case 1: Basic single pattern search
    print("1. SINGLE PATTERN SEARCH")
    print("-" * 30)
    text1 = "ABABDABACDABABCABCABCABCABC"
    pattern1 = "ABABCAB"

    matches = rk_small.search_single_pattern(text1, pattern1)
    print(f"Text: {text1}")
    print(f"Pattern: {pattern1}")
    print(f"Found at indices: {matches}")

    # Visualize matches
    for i, char in enumerate(text1):
        if i in matches:
            print(f"↑", end="")
        else:
            print(" ", end="")
    print(f"\n{text1}")
    print()

    # Test Case 2: Multiple pattern search
    print("2. MULTIPLE PATTERN SEARCH")
    print("-" * 30)
    text2 = "The quick brown fox jumps over the lazy dog. The fox is quick and brown."
    patterns = ["fox", "quick", "the", "brown", "lazy"]

    results = rk_small.search_multiple_patterns(text2, patterns)
    print(f"Text: {text2}")
    print("Patterns and their positions:")
    for pattern, positions in results.items():
        if positions:
            print(f"  '{pattern}': {positions}")
    print()

    # Test Case 3: Edge cases and collision demonstration
    print("3. EDGE CASES AND HASH COLLISIONS")
    print("-" * 40)

    # Edge case: Empty inputs
    print("Empty pattern test:", rk_small.search_single_pattern("hello", ""))
    print("Empty text test:", rk_small.search_single_pattern("", "hello"))

    # Pattern longer than text
    print("Pattern longer than text:", rk_small.search_single_pattern("hi", "hello"))

    # Demonstrate hash collision potential
    print("\nHash collision demonstration:")
    test_strings = ["AB", "BA", "CD"]  # These might have same hash with small prime
    for s in test_strings:
        hash_val = rk_small.compute_hash(s, len(s))
        print(f"Hash of '{s}': {hash_val}")
    print()

    # Test Case 4: Performance comparison with different parameters
    print("4. ALGORITHM ANALYSIS")
    print("-" * 25)

    import time

    # Large text for performance testing
    large_text = "ABCDEFGH" * 1000  # 8000 characters
    search_pattern = "EFGH"

    start_time = time.time()
    matches = rk_small.search_single_pattern(large_text, search_pattern)
    small_prime_time = time.time() - start_time

    start_time = time.time()
    matches = rk_large.search_single_pattern(large_text, search_pattern)
    large_prime_time = time.time() - start_time

    print(f"Performance on {len(large_text)} character text:")
    print(f"  Small prime (101): {small_prime_time:.6f} seconds")
    print(f"  Large prime (1009): {large_prime_time:.6f} seconds")
    print(f"  Pattern found {len(matches)} times")

    # Real-world application: DNA sequence matching
    print("\n5. REAL-WORLD APPLICATION: DNA SEQUENCE")
    print("-" * 45)
    dna_sequence = "ATCGATCGATCGTAGCTAGCTAGCATCGATCGAAAAATCGATCG"
    dna_patterns = ["ATCG", "TAGC", "AAAA", "CGAT"]

    dna_results = rk_small.search_multiple_patterns(dna_sequence, dna_patterns)
    print(f"DNA Sequence: {dna_sequence}")
    print("Found sequences:")
    for pattern, positions in dna_results.items():
        if positions:
            print(f"  {pattern}: positions {positions}")


# Additional utility functions for advanced usage
def compare_with_naive_search(text, pattern):
    """
    Compare Rabin-Karp with naive string matching for educational purposes
    """
    import time

    def naive_search(text, pattern):
        """Simple O(nm) string matching for comparison"""
        matches = []
        for i in range(len(text) - len(pattern) + 1):
            if text[i:i+len(pattern)] == pattern:
                matches.append(i)
        return matches

    # Time both algorithms
    rk = RabinKarp()

    start = time.time()
    rk_matches = rk.search_single_pattern(text, pattern)
    rk_time = time.time() - start

    start = time.time()
    naive_matches = naive_search(text, pattern)
    naive_time = time.time() - start

    print(f"Rabin-Karp: {len(rk_matches)} matches in {rk_time:.6f}s")
    print(f"Naive Search: {len(naive_matches)} matches in {naive_time:.6f}s")
    print(f"Results match: {rk_matches == naive_matches}")

    return rk_time, naive_time


if __name__ == "__main__":
    demonstrate_rabin_karp()

    print("\n" + "="*60)
    print("PERFORMANCE COMPARISON WITH NAIVE ALGORITHM")
    print("="*60)

    # Large text for meaningful comparison
    large_text = "ABCDEFGHIJKLMNOP" * 500  # 8000 characters
    test_pattern = "MNOP"

    rk_time, naive_time = compare_with_naive_search(large_text, test_pattern)
    speedup = naive_time / rk_time if rk_time > 0 else float('inf')
    print(f"Rabin-Karp is {speedup:.2f}x faster than naive search")

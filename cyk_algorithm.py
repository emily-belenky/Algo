def parse_rules(rules):
    """
    Parse the production rules into a dictionary for efficient lookup.
    :param rules: List of production rules in Chomsky Normal Form.
    :return: Dictionary mapping productions to variables.
    """
    productions = {}
    for rule in rules:
        left, right = rule.split("→")
        right = right.strip().split("|")
        for r in right:
            if r not in productions:
                productions[r] = []
            productions[r].append(left.strip())
    return productions

def cyk_algorithm(rules, word):
    """
    Implements the CYK algorithm to determine if a word belongs to a language.
    :param rules: List of production rules in Chomsky Normal Form.
    :param word: Input word to check.
    :return: True if the word belongs to the language, False otherwise.
    """
    productions = parse_rules(rules)
    n = len(word)
    if n == 0:
        return False

    # Initialize DP table
    dp = [[set() for _ in range(n)] for _ in range(n)]

    # Fill the diagonal of the DP table
    for i, char in enumerate(word):
        if char in productions:
            dp[i][i].update(productions[char])

    # Fill the table for substrings of length > 1
    for length in range(2, n + 1):  # Length of the substring
        for i in range(n - length + 1):  # Start index of the substring
            j = i + length - 1  # End index of the substring
            for k in range(i, j):  # Split point
                for B in dp[i][k]:
                    for C in dp[k + 1][j]:
                        if B + C in productions:
                            dp[i][j].update(productions[B + C])

    # Check if the start symbol 'S' is in the top-right cell
    return "S" in dp[0][n - 1]

# Example usage
if __name__ == "__main__":
    # Define the rules in Chomsky Normal Form
    rules = [
        "S→AX|BY|SS|AB|BA",
        "X→SB",
        "Y→SA",
        "A→a",
        "B→b",
    ]

    # Test cases
    test_words = [
        "abba",  # Example given in the question
        "abababababababababababababababab",  # Long word of length 30
        "babababababababababababababababa",  # Long word of length 30
        "aaabbbababababababababababababab",  # Long word of length 30
    ]

    for word in test_words:
        result = cyk_algorithm(rules, word)
        print(f"Word: {word}, Result: {result}")

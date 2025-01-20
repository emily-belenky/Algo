#Emily Belenky 314741877

import sys

def is_word_in_language(rules, word):
    """
    Determines if a given word is part of the language defined by the CFG in Chomsky Normal Form.
    
    :param rules: A dictionary where keys are variables and values are lists of possible productions.
    :param word: A string representing the input word.
    :return: True if the word is in the language, False otherwise.
    """
    n = len(word)
    if n == 0:
        return False
    
    # Initialize the DP table
    dp = [[set() for _ in range(n)] for _ in range(n)]
    
    # Base case: Fill single-character productions
    for i in range(n):
        for variable, productions in rules.items():
            if word[i] in productions:
                dp[i][i].add(variable)

    # Fill the table for substrings of length 2 to n
    for length in range(2, n + 1):
        for start in range(n - length + 1):
            end = start + length - 1
            for split in range(start, end):
                for variable, productions in rules.items():
                    for prod in productions:
                        if len(prod) == 2:  # Binary production
                            left, right = prod
                            if left in dp[start][split] and right in dp[split + 1][end]:
                                dp[start][end].add(variable)

    # Check if the start symbol 'S' generates the whole word
    return 'S' in dp[0][n - 1]


# Example grammar in Chomsky Normal Form
grammar_rules = {
    'S': ['AX', 'BY', 'SS', 'AB', 'BA'],
    'X': ['SB'],
    'Y': ['SA'],
    'A': ['a'],
    'B': ['b']
}

if __name__ == "__main__":
    # Check if words are provided as command-line arguments
    if len(sys.argv) < 2:
        print("Usage: python cyk_algorithm.py word1 word2 word3 ...")
        sys.exit(1)
    
    # Iterate through each word provided in the command-line arguments
    words = sys.argv[1:]
    for word in words:
        result = is_word_in_language(grammar_rules, word)
        print(f"'{word}': {result}")

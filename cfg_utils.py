from collections import defaultdict

def parse_cfg_rules(rules):
    """
    Parses the production rules into a dictionary.
    Each key is a non-terminal, and the value is a list of possible productions.
    """
    grammar = defaultdict(list)
    for rule in rules:
        head, body = rule.split(" -> ")
        body_parts = body.split(" | ")
        for part in body_parts:
            grammar[head].append(tuple(part.split()))
    return grammar

def cyk_algorithm(grammar, word):
    """
    CYK algorithm to determine if the word belongs to the language defined by the grammar.
    :param grammar: Dictionary representation of CFG in CNF.
    :param word: Input word to check.
    :return: True if the word belongs to the language, False otherwise.
    """
    n = len(word)
    if n == 0:
        return False  # Empty word not allowed unless grammar explicitly defines it

    # Initialize the DP table
    dp = [[set() for _ in range(n)] for _ in range(n)]

    # Fill the table for substrings of length 1
    for i, char in enumerate(word):
        for head, productions in grammar.items():
            for production in productions:
                if len(production) == 1 and production[0] == char:
                    dp[i][i].add(head)

    # Fill the table for substrings of length > 1
    for length in range(2, n + 1):  # length of substring
        for i in range(n - length + 1):
            j = i + length - 1  # endpoint of the substring
            for k in range(i, j):  # split point
                for head, productions in grammar.items():
                    for production in productions:
                        if len(production) == 2:  # Binary productions only
                            B, C = production
                            if B in dp[i][k] and C in dp[k + 1][j]:
                                dp[i][j].add(head)

    # Check if the start symbol 'S' generates the entire word
    return 'S' in dp[0][n - 1]

def main():
    # Example grammar in CNF
    rules = [
        "S -> AB | BC",
        "A -> BA | a",
        "B -> CC | b",
        "C -> AB | a"
    ]

    # Parse the rules into a grammar
    grammar = parse_cfg_rules(rules)

    # Test cases
    words = [
        "baaba",  # Should return True (belongs to the language)
        "aabbb",  # Should return False (does not belong)
        "abababababababababababababababab"  # Word of length 30
    ]

    print("Testing CYK Algorithm:")
    for word in words:
        result = cyk_algorithm(grammar, word)
        print(f"Word: '{word}', Belongs to Language: {result}")

if __name__ == "__main__":
    main()

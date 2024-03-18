import nltk

from typing import List


def recognize(grammar: nltk.grammar.CFG, sentence: List[str]) -> bool:
    """
    Recognize whether a sentence is in the language of grammar or not.

    Args:
        grammar: Grammar rule used to determine grammaticality of the sentence.
        sentence: Input sentence to be tested.

    Returns:
        truth_value: A bool value indicating whether the sentence
        is in the provided grammar or not.
    """
    # Create a chart to store intermediate parsing results
    chart = [[set() for _ in range(len(sentence) + 1)] for _ in range(len(sentence) + 1)]

    # Fill in the chart for the base case
    for i, word in enumerate(sentence):
        productions = grammar.productions(rhs=word)
        chart[i][i + 1] = {production.lhs() for production in productions}

    # Apply CKY algorithm to fill in the chart
    for width in range(2, len(sentence) + 1):
        for start in range(len(sentence) + 1 - width):
            end = start + width
            for mid in range(start + 1, end):
                for prod in grammar.productions():
                    if len(prod.rhs()) == 2:
                        B, C = prod.rhs()
                        if chart[start][mid].intersection({B}) and chart[mid][end].intersection({C}):
                            chart[start][end].add(prod.lhs())

    # Check if the start symbol is in the set of possible parses for the whole sentence
    return grammar.start() in chart[0][-1]
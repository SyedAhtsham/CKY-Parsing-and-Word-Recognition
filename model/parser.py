from typing import List, Set

import nltk


def parse(grammar: nltk.grammar.CFG, sentence: List[str]) -> Set[nltk.ImmutableTree]:
    """
    Check whether a sentence in the language of grammar or not. If it is, parse it.

    Args:
        grammar: Grammar rule that is used to determine grammaticality of sentence.
        sentence: Input sentence that will be tested.

    Returns:
        tree_set: Set of generated parse trees.
    """
    # Initialize the chart and backpointers
    chart = [[set() for _ in range(len(sentence) + 1)] for _ in range(len(sentence) + 1)]
    backpointers = [[dict() for _ in range(len(sentence) + 1)] for _ in range(len(sentence) + 1)]

    # Fill the diagonal of the chart with the terminal symbols
    for i, word in enumerate(sentence):
        for prod in grammar.productions(rhs=word):
            chart[i][i+1].add(prod.lhs())
            backpointers[i][i+1][prod.lhs()] = [prod.rhs()]

    # Apply the CKY algorithm
    for span in range(2, len(sentence) + 1):
        for start in range(len(sentence) + 1 - span):
            end = start + span
            for mid in range(start + 1, end):
                for prod in grammar.productions():
                    if len(prod.rhs()) == 2:
                        A, B = prod.rhs()
                        if A in chart[start][mid] and B in chart[mid][end]:
                            chart[start][end].add(prod.lhs())
                            if prod.lhs() not in backpointers[start][end]:
                                backpointers[start][end][prod.lhs()] = []
                            backpointers[start][end][prod.lhs()].append((A, B, mid))

    # Extract the parse trees
    def build_trees(symbol, start, end):
        trees = []
        if symbol in backpointers[start][end]:
            for rhs in backpointers[start][end][symbol]:
                if len(rhs) == 1:  # Terminal symbol
                    trees.append(nltk.ImmutableTree(symbol, [rhs[0]]))
                else:  # Non-terminal symbol
                    A, B, mid = rhs
                    for left_subtree in build_trees(A, start, mid):
                        for right_subtree in build_trees(B, mid, end):
                            trees.append(nltk.ImmutableTree(symbol, [left_subtree, right_subtree]))
        return trees

    return set(build_trees(grammar.start(), 0, len(sentence)))

def count(grammar: nltk.grammar.CFG, sentence: List[str]) -> int:
    """
    Compute the number of parse trees without actually computing the parse tree.

    Args:
        grammar: Grammar rule that is used to determine grammaticality of sentence.
        sentence: Input sentence that will be tested.

    Returns:
        tree_count: Number of generated parse trees.
    """
    # Initialize the chart
    chart = [[dict() for _ in range(len(sentence) + 1)] for _ in range(len(sentence) + 1)]

    # Fill the diagonal of the chart with the terminal symbols
    for i, word in enumerate(sentence):
        for prod in grammar.productions(rhs=word):
            chart[i][i+1][prod.lhs()] = 1

    # Apply the CKY algorithm
    for span in range(2, len(sentence) + 1):
        for start in range(len(sentence) + 1 - span):
            end = start + span
            for mid in range(start + 1, end):
                for prod in grammar.productions():
                    if len(prod.rhs()) == 2:
                        A, B = prod.rhs()
                        if A in chart[start][mid] and B in chart[mid][end]:
                            chart[start][end][prod.lhs()] = chart[start][end].get(prod.lhs(), 0) + chart[start][mid][A] * chart[mid][end][B]

    # Return the number of parse trees for the start symbol
    return chart[0][len(sentence)].get(grammar.start(), 0)
#######################################################################
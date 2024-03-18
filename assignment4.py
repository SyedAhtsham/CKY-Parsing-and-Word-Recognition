import argparse
import os
import time

import nltk
from nltk.draw import TreeWidget
from nltk.draw.util import CanvasFrame

from nltk.tree import Tree
from model.recognizer import recognize
from model.parser import parse, count

GRAMMAR_PATH = './data/atis-grammar-cnf.cfg'


def main():
    parser = argparse.ArgumentParser(
        description='CKY algorithm'
    )

    parser.add_argument(
        '--structural', dest='structural',
        help='Derive sentence with structural ambiguity',
        action='store_true'
    )

    parser.add_argument(
        '--recognizer', dest='recognizer',
        help='Execute CKY for word recognition',
        action='store_true'
    )

    parser.add_argument(
        '--parser', dest='parser',
        help='Execute CKY for parsing',
        action='store_true'
    )

    parser.add_argument(
        '--count', dest='count',
        help='Compute number of parse trees from chart without \
              actually computing the trees (Extra Credit)',
        action='store_true'
    )

    args = parser.parse_args()

    # load the grammar
    grammar = nltk.data.load(GRAMMAR_PATH)
    # load the raw sentences
    s = nltk.data.load("grammars/large_grammars/atis_sentences.txt", "auto")
    # extract the test sentences
    t = nltk.parse.util.extract_test_sentences(s)


    if args.structural:
        # YOUR CODE HERE
        #     TODO:
        #         1) Like asked in the instruction, derive at least two sentences that
        #         exhibit structural ambiguity and indicate the different analyses
        #         (at least two per sentence) with a syntactic tree.
        # Original Sentences
        sentences = ["Flights from Los Angeles to New York departing at 3 PM.", "Book a flight to Chicago arriving at 5 PM on Delta Airlines."]

        # Converted Sentences
        converted_sentences = [
            "(S (NP (Flights)) (PP (from (NP (Los Angeles to New York))) (VP (departing (PP (at (NP (3 PM))))))))",
            "(S (NP (Flights)) (PP (from (NP (Los Angeles to New York departing))) (PP (at (NP (3 PM))))))",
            "(S (VP (Book (NP (a flight to Chicago))) (PP (arriving (PP (at (NP (5 PM)))) (PP (on (NP (Delta Airlines))))))))",
            "(S (VP (Book (NP (a flight to Chicago arriving))) (PP (at (NP (5 PM on Delta Airlines))))))"
        ]

        # Display Trees
        tree1 = Tree.fromstring(converted_sentences[0])
        tree2 = Tree.fromstring(converted_sentences[1])
        print("Original Sentence:", sentences[0])
        print("Converted Trees:")
        tree1.pretty_print()
        print("\n" + "=" * 50 + "\n")
        tree2.pretty_print()
        print("\n" + "=" * 50 + "\n")
        print("\n" + "=" * 50 + "\n")

        tree1 = Tree.fromstring(converted_sentences[2])
        tree2 = Tree.fromstring(converted_sentences[3])
        print("Original Sentence:", sentences[1])
        print("Converted Trees:")
        tree1.pretty_print()
        print("\n" + "=" * 50 + "\n")
        tree2.pretty_print()
        print("\n" + "=" * 50 + "\n")




    elif args.recognizer:
        # YOUR CODE HERE
        #     TODO:
        #         1) Provide a list of grammatical and ungrammatical sentences (at least 10 each)
        #         and test your recognizer on these sentences.
        grammatical = [
            ['for', 'american', 'airlines', 'i', 'need', 'round', 'trip', 'airfare', 'from', 'new', 'york', 'to', 'san', 'diego', '.'],
            ["The", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog", "."],
            ["She", "saw", "a", "beautiful", "sunset", "at", "the", "beach", "."],
            ['what', 'is', 'the', 'duration', 'of', 'this', 'flight', '.'],
            ['please', 'list', 'the', 'costs', 'of', 'round', 'trip', 'fares', 'from', 'denver', 'to', 'atlanta', '.'],
            ['which', 'flights', 'are', 'cheapest', '.'],
            ['what', 'is', 'the', 'fare', '.'],
            ['i', 'can', 'only', 'spend', 'a', 'hundred', 'fifty', 'dollars', '.'],
            ['show', 'me', 'the', 'airlines', 'and', 'flight', 'numbers', '.'],
            ['what', 'flights', 'leave', 'los', 'angeles', 'arriving', 'in', 'minneapolis', '.'],
        ]

        ungrammatical = [
            ["This", "is", "an", "example", "ungrammatical", "sentence", "."],
            ["The", "cat", "on", "the", "roof", "is", "meow", "."],
            ['what', 'is', 'the', 'flying', 'time', 'from', '.'],
            ["Walking", "the", "through", "forest", "I", "enjoyed", "it", "."],
            ['i', 'am', 'only', 'spend', 'a', 'hundred', 'fifty', 'dollars', '.'],
            ['which', 'is', 'the', 'more', 'cheapest', 'flight', 'from', 'new', 'york', '.'],
            ['what', 'flights', 'does', 'leave', 'from', 'san', 'francisco', 'to', 'las', 'vegas', 'on', 'today', '.'],
            ['book', 'I', 'want', 'a', 'flight', 'to', 'seattle', 'next', 'friday', 'please', '.'],
            ['where', 'is', 'the', 'airplane', 'will', 'landing', 'in', 'new', 'orleans', '?'],
            ['the', 'which', 'cheapest', 'is', 'flight', 'from', 'boston', 'to', 'denver', '?'],
        ]

        for sents in grammatical:
            val = recognize(grammar, sents)
            if val:
                print("{} is in the language of CFG.".format(sents))
            else:
                print("{} is not in the language of CFG.".format(sents))

        for sents in ungrammatical:
            val = recognize(grammar, sents)
            if val:
                print("{} is in the language of CFG.".format(sents))
            else:
                print("{} is not in the language of CFG.".format(sents))

    elif args.parser:

        # We test the parser by using ATIS test sentences.
        print("ID\t Predicted_Tree\tLabeled_Tree")

        i=0
        total_execution_time = 0
        for idx, sents in enumerate(t):
            i += 1
            # Record start time
            start_time = time.time()

            tree_set = parse(grammar, sents[0])
            end_time = time.time()

            # Compute elapsed time
            elapsed_time = end_time - start_time
            total_execution_time += elapsed_time

            # Print the number of parses and labeled tree for each sentence
            print("{}\t {}\t \t{}".format(idx, len(tree_set), sents[1]))

            # Choose a sentence with a number of parses (p) such that 1 < p < 5
            if 1 < len(tree_set) < 5:

                # Select one of the parse trees for visualization
                selected_tree = next(iter(tree_set))

                # # Visualize the selected parse tree
                # print("\nVisualizing Parse Tree:")
                #
                # selected_tree.draw()

                # Create a new canvas frame
                cf = CanvasFrame()

                # Use TreeWidget to draw the tree on the canvas
                tc = TreeWidget(cf.canvas(), selected_tree)

                # Add the tree to the canvas
                cf.add_widget(tc, 10, 10)  # (10,10) offsets

                # Print the tree to a postscript file
                ps_filename = f'tree{i}.ps'
                cf.print_to_file(ps_filename)

                # Convert the postscript file to PNG
                png_filename = f'tree{i}.png'
                os.system(f'convert {ps_filename} {png_filename}')

                # Close the canvas
                cf.destroy()
        print(f"Execution time: {total_execution_time:.4f} seconds")
                # Break after the first sentence meeting the condition


    elif args.count:
        print("ID\t Predicted_Tree\tLabeled_Tree")
        total_execution_time = 0
        for idx, sents in enumerate(t):
            # Record start time
            start_time = time.time()
            num_tree = count(grammar, sents[0])
            end_time = time.time()
            # Compute elapsed time
            elapsed_time = end_time - start_time
            total_execution_time += elapsed_time
            print("{}\t {}\t \t{}".format(idx, num_tree, sents[1]))
        print(f"Execution time: {total_execution_time:.4f} seconds")


if __name__ == "__main__":
    main()

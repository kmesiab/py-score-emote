import argparse
import json
import os.path
import sys
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

output_file = "output.json"

# The string containing the raw input text to process
input_string = ""

# The list of punctuation marks that end a sentence
punctuations = ['.', '?', '!']

# The list of sentences to analyze
sentences = []

# The list of analyzed sentences
analyzed_sentences = []

# The usage notes for the program
usage_notes = "Usage: python emote-score.py -o <output_file> \"<input_string>\""


def validate_arguments():
    """
    Validate the command line arguments
    :return: True if the arguments are valid, False otherwise
    """
    parser = argparse.ArgumentParser(description="Process text and output the emotion scores for each sentence")

    parser.add_argument('-o', '--outfile', required=False, help="Output file (json format)")
    parser.add_argument('input_string', nargs='?', help="Input string")
    parsed_args = parser.parse_args()

    if parsed_args.input_string is None:
        print(usage_notes)
        exit(1)

    return parsed_args


def get_sentences(text):
    """
    Get the list of sentences from the input string
    :param text: The input string to analyze
    :return: The list of sentences
    """
    these_sentences = []
    this_sentence = ''
    for char in text:
        this_sentence += char
        if char in ['.', '?', '!']:
            these_sentences.append(this_sentence.strip())
            this_sentence = ''
    if this_sentence:
        these_sentences.append(this_sentence.strip())
    return sentences


def analyze_sentence(this_sentence):
    """
    Analyze the given sentence
    :param this_sentence: The sentence to analyze
    :return: The analyzed sentence
    """
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(this_sentence)

    return {
        "sentence": this_sentence,
        "vader_emotion_scores": scores
    }


if __name__ == '__main__':

    # Validate the command line arguments
    args = validate_arguments()

    # Set the input string and output file
    output_file = args.outfile
    input_string = args.input_string

    if input_string is None:
        input_string = sys.stdin.read().strip()
    else:
        print("Input string: " + input_string)

    # Split up the input string into sentences
    sentences = get_sentences(input_string)

    # Make sure we have sentences to analyze
    if len(sentences) == 0:
        print("No sentences to analyze")
        exit(1)

    # Analyze each sentence
    for sentence in sentences:
        analyzed_sentences.append(analyze_sentence(sentence))

    if len(analyzed_sentences) == 0:
        print("No sentences were analyzed")
        exit(1)

    outfile = open(output_file, "w")
    outfile.write(json.dumps(analyzed_sentences))

import argparse
import bs4
import os
import re
import requests
import signal
import sys
import unidecode

# determine if text is processed or not
PROCESSED_TEXT = False

# we can't split sentences on abbreviations that end in a '.'
ABB = [
    'etc', 'mr', 'mrs', 'ms', 'dr', 'sr',
    'jr', 'gen', 'rep', 'sen', 'st', 'al',
    'eg', 'ie', 'in', 'phd', 'md', 'ba',
    'dds', 'ma', 'mba', 'inc', 'pm', 'am',
    'jan', 'feb', 'mar', 'apr', 'jun', 'jul',
    'aug', 'sep', 'sept', 'oct', 'nov', 'dec',
    'mon', 'tue', 'wed', 'weds', 'thur',
    'thu', 'thurs', 'fri', 'fig'
]

# if we come across a word with a '.' that ends in one of these common file
# extensions, we should not split on the '.'
EXT = [
    'js', 'py', 'txt', 'json', 'doc', 'docx', 'pdf',
    'bash', 'sh', 'java', 'jsx', 'html', 'css', 'db',
    'md', 'csh', 'zsh', 'xsh', 'cpp', 'swift', 'gpg',
    'pickle', 'png', 'jpg', 'jpeg', 'gif', 'tiff', 'lock',
    'rb', 'git', 'gitignore', 'ico', 'webmanifest',
    'icns', 'xls', 'xlsx', 'ppt', 'pptx', 'asp', 'aspx',
    'yaws', 'pl', 'php', 'xml', 'svg', 'heic', 'mov',
    'bz2', 'csv', 'cs', 'erl', 'asm', 'awk', 'bat', 'bmp',
    'class', 'dll', 'dump', 'exe', 'hpp', 'jar', 'log', 
    'obj', 'rc', 'ts', 'rs', 'wav', 'zip', 'com', 'nl',
    'ms'
]

# we should exclude these common words when scoring sentences to get more
# accurate sentence scores
EXCLUDE = [
    'the', 'of', 'to', 'a', 'and', 'in', 'that',
    'he', 'she', 'on', 'as', 'his', 'hers', 'for',
    'is', 'by', 'was', 'with', 'at', 'from', 'has',
    'its', 'mr', 'mrs', 'ms', 'dr', 'sr', 'jr',
    'sen', 'rep', 'st', 'said', 'it', 'be', 'not',
    'or', 'but', 'who', 'when', 'your', 'those',
    'these', 'you', 'this', 'they', 'we', 'our',
    'will', 'are', 'am', 'can', 'an', 'have', 'how',
    'my', 'which', 'their', 'theirs', 'what', 'her',
    'him', 'had', 'would', 'them', 'like', 'than',
    'could', 'did', 'do'
]

# if we see a lot of these symbols, the sentence is likely code and should
# be ignored
CODE = [
    '{', '}', '=', '[', ']', '/', '\\', '@', ':',
    '<', '>', '!', '|', '*', '+', '-', ';', '?',
    '(', ')', '$', '&', '%', '^', '_', '#', '~',
    '`'
]

# strip away these tags from the HTML to attempt to pull out meaningful text
# content in these tags is usually not relevant to text meaning
TAGS = [
    'script', 'style', 'h1', 'h2', 'h3', 'h4',
    'h5', 'h6', 'nav', 'title', 'svg', 'footer'
]

# if a tag has a class with one of these key words, it is usually not
# relevant to text meaning
CLASS_KEYWORDS = [
    'nav', 'menu', 'copyright'
]

# custom exception for when timeouts occur
class TimeoutException(Exception):
    pass

# try to pull text out of source
def get_text(source):
    text = None
    status_code = None
    global PROCESSED_TEXT

    # read text from file or URL
    if os.path.isfile(source):
        # update timeout settings
        PROCESSED_TEXT = True
        status_code = 200
        try:
            with open(source) as f:
                text = f.read()
        except:
            print(f'Could not read from local file \'{source}\'')
            sys.exit(1)
    else:
        try:
            # get HTML from webpage
            html = requests.get(source)
            status_code = html.status_code

            # convert HTML to meaningful text data with 3 steps
            #  1. convert HTML to plaintext
            #  2. remove irrelevant tags
            #  3. remove navigation links
            soup = bs4.BeautifulSoup(html.content, 'html.parser')
            for script in soup(TAGS):
                script.extract()
            for tag in soup.find_all():
                if 'class' in tag.attrs:
                    for class_name in CLASS_KEYWORDS:
                        if class_name in ' '.join(tag.attrs['class']).lower():
                            tag.extract()
            text = soup.get_text()

            # update timeout settings
            PROCESSED_TEXT = True
        except TimeoutException:
            sys.exit(1)
        except:
            print(f'Could not fetch data from URL')
            sys.exit(1)

    if not status_code == 200:
        print(f'({status_code}) Could not scrape data, unable to access data programmatically from URL')
        sys.exit(1)

    # decode text to ASCII-ish
    try:
        text = unidecode.unidecode(text)
    except:
        print(f'Could not decode parsed data')
        sys.exit(1)

    # replace persnickity characters
    text = text.replace('\n', ' ').replace(' " ', ' ').replace(" ' ", ' ')
    if text == '' or text == None or not '.' in text:
        print(f'Could not parse text, either no sentences found in data or data format could not be processed')
        sys.exit(1)
    return text

# build resolved sentences from a block of text
def get_sentences(text):
    sentences = [chunk for chunk in re.split('([.?!])', text) if not chunk == '' and not chunk.isspace()]
    sentences = [x+y for x,y in zip(sentences[0::2], sentences[1::2])]

    # we'll need to make sure we split up our sentences properly based on ABB and EXT
    index = 0
    while index < len(sentences) - 2:
        last_word_previous_sentence = ''.join(character for character in sentences[index].split()[-1].lower() if character.isalnum()).lower()
        first_word_next_sentence = ''.join(character for character in sentences[index+1].split()[0].lower() if character.isalnum()).lower()
        if (
            last_word_previous_sentence in ABB
            or first_word_next_sentence in EXT
            or len(last_word_previous_sentence) == 1
            or len(first_word_next_sentence) == 1
        ) and (
            not last_word_previous_sentence in ['a', 'i']
            and not first_word_next_sentence in ['a', 'i']
        ):
            sentences[index] = ''.join([sentences[index], sentences[index + 1]])
            del sentences[index + 1]
        else:
            index += 1
    return [sentence.strip() for sentence in sentences]

# calculate how frequently each word occurs in the text
# we want to ignore the words in EXCLUDE
def calculate_word_frequency(sentences):
    frequencies = {}
    words = ' '.join(sentences).split()
    raw_words = [''.join(character for character in word if character.isalnum()).lower() for word in words]
    for word in raw_words:
        if word in EXCLUDE:
            frequencies[word] = 0
        elif word in frequencies:
            frequencies[word] += 1
        else:
            frequencies[word] = 1

    if '' in frequencies:
        del frequencies['']
    return frequencies

# calculate the score for each sentence depending on its word contents
def calculate_sentence_scores(sentences, frequencies):
    scores = []
    for sentence in sentences:
        score = 0
        if sum(map(sentence.count, CODE)) >= 10:
            scores.append(score)
            continue

        for word in sentence.split():
            raw_word = ''.join(character for character in word if character.isalnum()).lower()
            if raw_word == '':
                continue
            score += frequencies[raw_word]
        scores.append(score)

    # weight first 10% of text 50% heavier, as most news articles are front-loaded
    sentence_scores = list(zip(sentences, scores))
    for index in range(int(len(sentence_scores)*0.1)):
        sentence_scores[index] = (sentence_scores[index][0], int(sentence_scores[index][1]*1.5))
    return sentence_scores

# build the summary string based on the most important sentences
def build_summary(scores, limit):
    # build list of sentence indicies
    sentence_indices = []
    for index, score in enumerate(scores):
        sentence_indices.append((index, score[1]))

    # sort based on sentence score
    sorted_sentences = sorted(sentence_indices, key=lambda item: item[1])[::-1]

    # build list of highest ranked sentences
    summary_sentences = []
    for index in range(limit):
        if index < len(scores) - 1:
            summary_sentences.append(scores[sorted_sentences[index][0]][0])

    # clean up text and convert to string
    # ~94% of English words are less than 14 characters, so we exclude words
    # longer than 14 characters to attempt to further clarify the text
    summary = ' '.join(summary_sentences)
    summary = ' '.join([word for word in summary.split() if len(word) < 14])
    return summary

# build the metrics string based on summary properties
def build_metrics(text, summary, frequencies, omit, verbose):
    metrics = ''
    if omit:
        return metrics
    
    original_length = len(text)
    smooshed_length = len(summary)
    smooshed_percentage = (1.0 - (float(smooshed_length) / float(original_length))) * 100
    smooshed_percentage = '%.2f' % smooshed_percentage
    metrics += '-_-_-_-_-_-_ METRICS _-_-_-_-_-_-\n'
    metrics += f'Original length: {original_length} characters\n'
    metrics += f'Smooshed length: {smooshed_length} characters\n'
    metrics += f'Original smooshed by {smooshed_percentage}%'
    if not verbose:
        return metrics

    most_common_words = sorted(frequencies.items(), key=lambda item: item[1])[-5:][::-1]
    most_common_words = [
        word if not word[0] == 'i' else ('I', word[1])
        for word
        in most_common_words
    ]
    metrics += '\nMost common words:\n'
    metrics += f' * {most_common_words[0][0]} ({most_common_words[0][1]} time{"" if most_common_words[0][1] == 1 else "s"})\n'
    metrics += f' * {most_common_words[1][0]} ({most_common_words[1][1]} time{"" if most_common_words[0][1] == 1 else "s"})\n'
    metrics += f' * {most_common_words[2][0]} ({most_common_words[2][1]} time{"" if most_common_words[0][1] == 1 else "s"})\n'
    metrics += f' * {most_common_words[3][0]} ({most_common_words[3][1]} time{"" if most_common_words[0][1] == 1 else "s"})\n'
    metrics += f' * {most_common_words[4][0]} ({most_common_words[4][1]} time{"" if most_common_words[0][1] == 1 else "s"})'
    return metrics

# print the final results
def print_results(summary, metrics):
    print(summary)
    if not metrics == '':
        print('')
        print(metrics)

# build the command line parser
def build_parser():
    parser = argparse.ArgumentParser(description='Summarize any text article', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('source', type=str, help='the text source, which can either be the path to a local file or a URL to a webpage')
    parser.add_argument('-n', '--sentence-limit', type=int, default=7, required=False, help='the number of sentences that will be used to describe the text')
    parser.add_argument('-q', '--quiet', action='store_true', required=False, help='omit metric summary')
    parser.add_argument('-v', '--verbose', action='store_true', required=False, help='print verbose metric summary')
    parser.add_argument('-t', '--timeout', type=int, default=10, required=False, help='timeout (in seconds) to use when fetching data from a URL')
    return parser

# raise an exception if timeout occurs
def signal_handler(signum, frame):
    raise TimeoutException('timeout')

def main():
    # parse args
    parser = build_parser()
    args = parser.parse_args()

    # set up timeout
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(args.timeout)

    try:
        text = get_text(args.source)
        sentences = get_sentences(text)
        frequencies = calculate_word_frequency(sentences)
        scores = calculate_sentence_scores(sentences, frequencies)
        summary = build_summary(scores, args.sentence_limit)
        metrics = build_metrics(text, summary, frequencies, args.quiet, args.verbose)
        print_results(summary, metrics)
    except:
        if not PROCESSED_TEXT:
            print(f'Timeout occurred while trying to fetch data from URL')
            sys.exit(1)
        sys.exit(1)

if __name__ == '__main__':
    main()

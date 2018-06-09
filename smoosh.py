#!/lib/bin/python

import sys
import argparse
from argparse import RawTextHelpFormatter

ABB = ['etc', 'mr', 'mrs', 'ms', 'dr', 'sr', 'jr', 'gen', 'rep', 'sen', 'st', 'al', 'eg', 'ie', 'in', 'phd', 'md', 'ba', 'dds', 'ma', 'mba', 'us', 'usa']

def extract_words(filename):
  f = open(filename, 'rU')
  text_ = f.read()
  text = text_.replace('\n', ' ')
  f.close()
  
  filesize = len(text)
  words = text.split()
  cleaned_words = clean_text(words)[::-1]

  sentences = []
  str_buffer = ''

  # EOS = end of sentence
  ## checking for EOS
  ## if EOS --> append to buffer ('.'), add buffer to array, clear buffer
  ## if !EOS --> append to buffer
  for index, ch in enumerate(text):
    if ch == '?' or ch == '!':
      if text[index+1] == ' ':
        # EOS
        str_buffer += ch
        sentences.append(str_buffer)
        str_buffer = ''
      else:
        # !EOS
        str_buffer += ch
    elif ch == '.':
      if text[index+1] == ' ':
        if isAbbreviation(str_buffer):
          # !EOS
          str_buffer += ch
        elif text[index+2].upper() == text[index+2]:
          # EOS
          str_buffer += ch
          sentences.append(str_buffer)
          str_buffer = ''
      else:
        # !EOS
        str_buffer += ch
    else:
      # !EOS
      str_buffer += ch

  return (filesize, sentences, sorted(count_words(cleaned_words).items(), key=custom_sort))

def isAbbreviation(text):
  search = text[::-1]
  buff = ''

  for ch in search:
    if not ch == ' ':
      buff += ch
    else:
      break

  buff = buff[::-1]
  buff = buff.lower()
  buff = buff.replace('.', '')

  if buff in ABB:
    return True
  else:
    return False

def custom_sort(s):
  return s[-1]

def clean_text(words):
  cleaned_words = []

  for word in words:
    cleaned_word = word
    cleaned_word.replace('"', '')
    # do more cleaning here
    cleaned_word = cleaned_word.lower()
    cleaned_words.append(cleaned_word)

  return cleaned_words

def count_words(words):
  word_count = {}
  for word in words:
    if word in word_count:
      word_count[word] += 1
    else:
      word_count[word] = 1

  return word_count

def assign_word_scores(word_list):
  counts_ = map(list, zip(*word_list))[1]
  counts = sorted(list(set(counts_)))

  scores = {}
  for index, count in enumerate(counts):
    scores[count] = index+1

  word_scores = {}
  for word, occurrence in word_list:
    word_scores[word] = scores[occurrence]

  return word_scores

def assign_sentence_scores(sentences, word_scores):
  score = 0
  scores = {}
  for index, sentence in enumerate(sentences):
    words = sentence.split()
    cleaned_words = clean_text(words)
    for word in cleaned_words:
      score += word_scores[word]
    scores[index] = score
    score = 0

  return scores
      
def parse():
  parser = argparse.ArgumentParser(description='\tsmoosh \n\t/smooSH/ (verb) to squash, crush, or flatten\n\n\tSummarizes a text file', formatter_class=RawTextHelpFormatter)

  parser.add_argument('-n', '--number-of-sentences', type=int, help='the number of sentences that will be used to describe the text (default is 7)', required=False)
  parser.add_argument('-f', '--file', help='if included, output will be written to \'output.txt\'', action='store_true')
  parser.add_argument('-o', '--omit-metrics', help='if included, metric summary will be ommitted', action='store_true')
  parser.add_argument('filename', type=str, help='the name of the file to be summarized (as a .txt file)')

  args = parser.parse_args()
  if args.number_of_sentences:
    if args.number_of_sentences < 5:
      print 'WARNING: defaulting to minimum number of sentences, which is 5...'
      num_of_sentences = 5
    elif args.number_of_sentences > 10:
      print 'WARNING: defaulting to maximum number of sentences, which is 10...'
      num_of_sentences = 10
    else:
      num_of_sentences = args.number_of_sentences
  else:
    num_of_sentences = 7

  if args.file:
    write_to_file = True
  else:
    write_to_file = False

  if args.omit_metrics:
    omit_metrics = True
  else:
    omit_metrics = False

  if args.filename:
    filename = args.filename
  else:
    print 'ERROR: no filename provided\nUse smoosh.py -h for help'
    sys.exit(0)

  return (num_of_sentences, write_to_file, omit_metrics, filename)

def main():
  # grab + parse cmd line arguments
  (num_of_sentences, write_to_file, omit_metrics, filename) = parse()

  # read from file and score sentences
  (filesize, sentences, word_list) = extract_words(filename)
  word_scores = assign_word_scores(word_list)
  sentence_scores = assign_sentence_scores(sentences, word_scores)

  # sort top sentences
  final_scores = sorted(sentence_scores.items(), key=custom_sort)[::-1]
  top_sentence_ids = []
  for index in range(num_of_sentences):
    top_sentence_ids.append(final_scores[index][0])
  top_sentence_ids.sort()

  # build new smoosh
  smoosh = ''
  for index in range(num_of_sentences):
    smoosh += sentences[index]
        
  smooshsize = len(smoosh)
  smoosh_percentage_ = 1.0 - (float(smooshsize) / float(filesize))
  smoosh_percentage = '%.2f' % smoosh_percentage_

  summary =  """
-_-_-_-_-_-_ METRICS _-_-_-_-_-_-
Original length: {0} characters
Smooshed length: {1} characters

Original smooshed by {2}%
""".format(filesize, smooshsize, smoosh_percentage)

  if write_to_file:
    f = open('output.txt', 'w')
    f.write(smoosh)
    f.write('\n')
    if not omit_metrics: f.write(summary)
    f.close()
  else:
    print smoosh
    if not omit_metrics: print summary

if __name__ == '__main__':
  main()


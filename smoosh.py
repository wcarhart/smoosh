#!/lib/bin/python

import sys
import re

ABB = ['etc', 'mr', 'mrs', 'ms', 'dr', 'sr', 'jr', 'gen', 'rep', 'sen', 'st', 'al', 'eg', 'ie', 'in', 'phd', 'md', 'ba', 'dds', 'ma', 'mba', 'us', 'usa']

def extract_words(filename):
  f = open(filename, 'rU')
  text_ = f.read()
  text = text_.replace('\n', ' ')
  f.close()

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

  for index, sentence in enumerate(sentences):
    print str(index) + ": " + sentence

  #print sorted(count_words(cleaned_words).items(), key=custom_sort)

  return text

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





def main():
  if len(sys.argv) != 2:
    print 'usage: python smmry.py filename.txt'
    sys.exit(1)

  word_list = extract_words(sys.argv[1])

  #print word_list



if __name__ == '__main__':
  main()


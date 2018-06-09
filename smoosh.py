#!/lib/bin/python

import sys
import re

def extract_words(filename):
  f = open(filename, 'rU')
  text = f.read()
  f.close()

  words = text.split()
  cleaned_words = clean_text(words)[::-1]

  sentences = []
  str_buffer = ''

  for ch in text:
    if ch == '.' or ch == '?' or ch == '!':
      balh
    else:
      


  sentences = text.split('.')
  print sentences

  #print sorted(count_words(cleaned_words).items(), key=custom_sort)

  return text

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


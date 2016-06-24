#! /usr/bin/env python3
# coding: utf-8

import re
import os
import sys


PATH = sys.argv[1]

LETTER_MIN = 3
WORD_MIN = 2
WORD_MAX = 3
DIFF_MAX = 1
POPULAR_MIN = 12


# TODO: apply language-specific filters


def simplify_text(text):
    text = text.lower()
    
    # all end-phrase replace with dot
    text = text.replace('\n', '.')
    text = text.replace('?', '.')
    text = text.replace('!', '.')
    text = text.replace(',', '.')
    
    # all non-letter an not '- replace with space
    text = re.sub("(?!'|-|\.)\W", ' ', text)
    return text


def read_path(path):
    lines = []
    if os.path.isdir(path):
        # TODO: read all files in dir
        lines = []
    else:
        with open(path) as textfile:
            lines += textfile.readlines()
    text = ''.join(lines)
    return simplify_text(text)


def get_uniq_words(text):
    text = re.sub("(?!'|-)\W", ' ', text)
    words = set(text.split())
    return words


def get_similar_words(uniq_words, word):
    global DIFF_MAX
    similar_words = []
    uniq_words = [it for it in uniq_words if len(it) == len(word)]
    
    for uniq_word in uniq_words:
        diff_count = sum(uniq_word[i] != word[i] for i in range(len(word)))
        if 1 <= diff_count <= DIFF_MAX:
            similar_words.append(uniq_word)
    return similar_words


def get_uniq_phrases(text):
    # TODO: split to two functions
    global WORD_MIN, WORD_MAX, LETTER_MIN, POPULAR_MIN
    uniq_phrases = set()
    
    for sentence in [it for it in re.split('\.', text) if it]:
        for word_count in range(WORD_MIN, WORD_MAX+1):
            sentence_splitted = sentence.split()
            sentence_len = len(sentence_splitted)
            if sentence_len >= word_count:
                for i in range(0, sentence_len-word_count+1):
                    phrase = sentence_splitted[i:i+word_count]
                    if all(len(word) >= LETTER_MIN for word in phrase):
                        uniq_phrases.add(' '.join(phrase))
    uniq_phrases = [it for it in uniq_phrases if text.count(it) >= POPULAR_MIN]
    return uniq_phrases


def main():
    global PATH
    print('analyzing...\n')
    
    text = read_path(PATH)
    uniq_words = get_uniq_words(text)
    print_block = []

    for phrase in get_uniq_phrases(text):
        print_block.append(phrase)
        for word in phrase.split():
            for similar_word in get_similar_words(uniq_words, word):
                pun = phrase.replace(word, similar_word)
                print_block.append('\t' + pun)
        if len(print_block) >= 2:
            for item in print_block:
                print(item)
        print_block = []


if __name__ == '__main__':
    main()

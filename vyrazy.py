#! /usr/bin/env python3
# coding: utf-8
import sys

#~ alphabet = 'ёйцукенгшўзхфывапролджэячсмітьбю'	#~ bel
alphabet = 'ёйцукенгшщзхъфывапролджэячсмитьбю'		#~ rus
vows = 'ёуеыаоэяию'		#~ rus vows
infile = sys.argv[1]

def get_similars(word, gain):
	res = []
	for letter in alphabet:
		for idx_lw, wordletter in enumerate(word):
			newword = word[:idx_lw] + letter + word[idx_lw+1:]
			if len(newword) < gain: continue
			#~ if newword[:-1] == word[:-1] and word[-1] in vows: continue
			if newword[:-1] == word[:-1]: continue
			if word.startswith('котор'): continue
			#~ if newword[:-1] == word[:-1] and newword in uniqwords: res.append(newword)
			if newword in uniqwords: res.append(newword)
	return res

def get_newvyraz(vyraz, wordidx, newword):
	newvyraz = vyraz[:].split()
	newvyraz[wordidx] = newword
	return ' '.join(newvyraz)

def make_couples(words, number):
	res = []
	for idx in range(len(allwords) - (number-1)):
		res.append(words[idx:idx+number])
	return res


if __name__ == '__main__':
	
	#~ make word lists
	allwords = []
	uniqwords = []
	for line in open(infile):
		line = line.lower()
		line = line.replace('ё', 'е') #~ if russian
		word = ''
		for char in line:
			if char in alphabet:
				word += char
			else:
				if word:
					allwords.append(word)
					if word not in uniqwords: uniqwords.append(word)
				word = ''
	
	#~ make vyrazy
	allvyrazy = []
	uniqvyrazy = {}
	for number in (2,3,4):
		for couple in make_couples(allwords, number):
			allvyrazy.append(' '.join(couple))
			uniqvyrazy[' '.join(couple)] = 0
	for vyraz in allvyrazy:
		uniqvyrazy[vyraz] += 1
	
	
	#~ main cycle
	for vyraz in uniqvyrazy:
		firsttime = True
		if uniqvyrazy[vyraz] > 20:
			for idx, word in enumerate(vyraz.split()):
				for similar in get_similars(word, gain = 4):
					newvyraz = get_newvyraz(vyraz, wordidx=idx, newword=similar)
					if newvyraz != vyraz:
						if firsttime:
							print('> ' + vyraz)
							firsttime = False
						print(newvyraz)

# 6.00 Problem Set 3
# 
# Hangman
#


# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
import random
import string

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = string.split(line)
    print "  ", len(wordlist), "words loaded."
    return wordlist

def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code
# -----------------------------------

# actually load the dictionary of words and point to it with 
# the wordlist variable so that it can be accessed from anywhere
# in the program
wordlist = load_words()

# your code begins here!

'''def fucntions'''
def guessed_string_function(c,s,gs):
    temp_string = gs
    x = 0
    for i in s:
        if c == i:
            temp_string = temp_string[0:x] + c + temp_string[x+1:]
        x += 1
    return temp_string

def remaining_letter(c,s):
    temp_string = s
    x = 0
    for i in s:
        if c == i:
            temp_string = temp_string[0:x] + temp_string[x+1:]
        x += 1
    return temp_string
        

win = 0       
word = choose_word(wordlist)
alphabet_string = 'abcdefghijklmnopqrstuvwxyz'
guessed_string = ''
for s in range(0,len(word)):
    guessed_string = guessed_string + '_'
guesses = 8
word_tuple = tuple()
for i in word:
    word_tuple += i,

    



print 'Welcome to the game, Hangman!'
print 'I am thinking of a word that is %i letters long.' %len(word)
print '--------'
while guesses > 0 and win == 0:
    lettertest = True
    print 'You have %i guesses left.' % guesses
    print 'Available letters:', alphabet_string
    while lettertest == True and win == 0:
        letter = raw_input('Please guess a letter: ')
        if letter in alphabet_string:
            if letter in word:
                guessed_string = guessed_string_function(letter,word,guessed_string)
                print 'Good guess: ', guessed_string
                alphabet_string = remaining_letter(letter,alphabet_string)
            else:
                print 'Oops! That letter is not in my word: ', guessed_string
                guesses = guesses - 1
                alphabet_string = remaining_letter(letter,alphabet_string)
        else:
            print 'You\'ve already used that letter'
            continue
        print '--------'
        if '_' in guessed_string:
            lettertest = False
        else: win = 1
    
if win == 1:
    print 'Congratulations, you won!'
else: print 'You\'re man has been hanged'




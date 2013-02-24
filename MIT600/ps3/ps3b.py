from ps3a import *
import time
from perm import *


#
#
# Problem #6A: Computer chooses a word
#
#
def comp_choose_word(hand, word_list):
    """
	Given a hand and a word_dict, find the word that gives the maximum value score, and return it.
   	This word should be calculated by considering all possible permutations of lengths 1 to HAND_SIZE.

    hand: dictionary (string -> int)
    word_list: list (string)
    """
    # TO DO...
    score = 0
    saved = 0
    saved_score = 0
    for i in range(len(hand), 0, -1):
        useable_word_list = get_perms(hand, i)
        for word in useable_word_list:
            if word in word_list:
                score = get_word_score(word, HAND_SIZE)
                if saved_score == 0:
                    saved_word = word
                    saved = 1
                    saved_score = score
                    continue
                elif score > saved_score:
                    saved_score = score
                    saved_word = word
                    saved = 1
    if saved == 1:
        return saved_word
                
#
# Problem #6B: Computer plays a hand
#
def comp_play_hand(hand, word_list):
    """
     Allows the computer to play the given hand, as follows:

     * The hand is displayed.

     * The computer chooses a word using comp_choose_words(hand, word_dict).

     * After every valid word: the score for that word is displayed, 
       the remaining letters in the hand are displayed, and the computer 
       chooses another word.

     * The sum of the word scores is displayed when the hand finishes.

     * The hand finishes when the computer has exhausted its possible choices (i.e. comp_play_hand returns None).

     hand: dictionary (string -> int)
     word_list: list (string)
    """
    # TO DO ...
    word_score = 0
    total_score = 0
    
    while True:
        print "Current Hand:",
        display_hand(hand)
        print "Computer thinking"
        word = comp_choose_word(hand, word_list)
        if word == None:
            break
        elif is_valid_word(word, hand, word_list):
            word_score = get_word_score(word, HAND_SIZE)
            total_score += word_score
            print '\"' + word + '\" earned', word_score, 'points. Total:', total_score, 'points'
            hand = update_hand(hand, word)
            if calculate_handlen(hand) == 0:
                break
        else: print 'Invalid word, please try again.'
    print 'Total score:', total_score ,'points.'
    
#
# Problem #6C: Playing a game
#
#
def play_game(word_list):
    """Allow the user to play an arbitrary number of hands.

    1) Asks the user to input 'n' or 'r' or 'e'.
    * If the user inputs 'n', play a new (random) hand.
    * If the user inputs 'r', play the last hand again.
    * If the user inputs 'e', exit the game.
    * If the user inputs anything else, ask them again.

    2) Ask the user to input a 'u' or a 'c'.
    * If the user inputs 'u', let the user play the game as before using play_hand.
    * If the user inputs 'c', let the computer play the game using comp_play_hand (created above).
    * If the user inputs anything else, ask them again.

    3) After the computer or user has played the hand, repeat from step 1

    word_list: list (string)
    """
    # TO DO...
    iterations = 0
    while True:
        print "Enter 'n' to play a new (random) hand"
        if iterations > 0:
            print "Enter 'r' to play the last hand again"
        print "Enter 'e' to exit the game"
        input_word = raw_input('***')
        if input_word == 'n':
            while True:
                hand = deal_hand(HAND_SIZE)
                input_word = raw_input("Enter 'u' for user to play hand or 'c' for computer to play it")
                if input_word == 'u':
                    play_hand(hand, word_list)
                    break
                elif input_word == 'c':
                    comp_play_hand(hand, word_list)
                    break
                else: print
        elif input_word == 'r' and iterations > 0:
            while True:
                input_word = raw_input("Enter 'u' for user to play hand or 'c' for computer to play it")
                if input_word == 'u':
                    play_hand(hand, word_list)
                    break
                elif input_word == 'c':
                    comp_play_hand(hand, word_list)
                    break
                else: print
        elif input_word == 'e':
            break
        else: print
        iterations += 1
        
#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)

    

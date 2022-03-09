#!/bin/python3
import string
import time
import unidecode
import os
import sys
import random
from signal import signal, SIGINT


def handler(sig, frame):
    print("\n\n" + colors.RED + "Saliendo...\n")
    end(False, wordToGuess)

class colors:
    UNDERLINE = '\033[4m'
    CYAN = '\033[96m'
    ENDC = '\033[0m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'

def prettyPrint(word, matches):
    green = matches[0]
    yellow = matches[1]
    
    for i, c in enumerate(word):
        if i in green:
            print(colors.GREEN + c.upper(), end='')        
        elif i in yellow:
            print(colors.YELLOW + c.upper(), end='')
        else:
            print(colors.ENDC + c.upper(), end='')
        sys.stdout.flush()
        time.sleep(.2)
    print()
def loadDic(path):
    file = open(path, 'r')
    words = file.read()
    file.close()
    return words.split('\n')

def removeAccents(dic):
    dicn = []
    for w in dic:
        dicn.append(unidecode.unidecode(w))

    return dicn

def selectRandomWord(dic):
    return random.choice(dic)

def matchWords(word):

    green = []
    yellow = []
    wordToGuessC = wordToGuess
    wordC = word

    for i, c in enumerate(word):
        if c == wordToGuess[i]:
            green.append(i)
            wordToGuessC = wordToGuessC[:i] + ' ' + wordToGuess[i + 1:]
            wordC = wordC[:i] + '.' + wordC[i + 1:]
    
    for i, c in enumerate(wordC):
        if c in wordToGuessC:
            yellow.append(i) 
            wordToGuessC = wordToGuessC.replace(c, ' ', 1)
    
    return (green, yellow)

def end(victory, word):
    if victory: print(colors.GREEN + "¡Has ganado!")
    else: print(colors.RED + "Has perdido, la palabra era: " + colors.YELLOW + colors.BOLD + word)
    exit(0)

if __name__ == "__main__":

    dic = loadDic("./dic/five-letter-spanish-common.txt")
    fullDic = removeAccents(loadDic("./dic/five-letter-spanish-full.txt"))

    global wordToGuess
    wordToGuess = unidecode.unidecode(selectRandomWord(dic).lower())
    signal(SIGINT, handler)

    os.system('clear')
    print(colors.CYAN + colors.UNDERLINE + colors.BOLD + "\n===== WORDLE =====" + colors.ENDC)
    
    userWords = []

    for i in range(6):
        while True:
            word = unidecode.unidecode(input(colors.ENDC + '>> ').lower())
            print ("\033[A                             \033[A")
            if word == "": continue
            if (word in fullDic or word in dic) and word not in userWords:
                break

        print(colors.CYAN + str(i+1) + ". ", end="")
        sys.stdout.flush()
        time.sleep(0.2)
        prettyPrint(word, matchWords(word))
        userWords.append(word)
        if word == wordToGuess:
            end(True, wordToGuess)

    end(False, wordToGuess)


#!/usr/bin/env python3
import random
from os import system
from glob import glob
from gtts import gTTS
from io import BytesIO
from playsound import playsound
clear = lambda: system('clear')

def say(speech):
    """Accepts a string and converts to speech writing to speech.mp3 and playing the file"""
    tts = gTTS(speech)
    tts.save('speech.mp3')
    playsound('speech.mp3')

def read_words():
    """Lists all *.txt files in the directory and allows a test file to be chosen"""
    clear()
    print("**********************")
    print("*                    *")
    print("*   Test Selection   *")
    print("*                    *")
    print("**********************\n")
    AvailableTests = glob('*.txt')    # Read in text file names from local directory
    # Quit if no test files are located in the local directory
    if len(AvailableTests) == 0:
        print("No test files available")
        quit()
    
    #Display available test files
    print("The following test files are available:")
    count = 1
    for TestFile in AvailableTests:
        print(str(count) + '.', TestFile)
        count += 1
    print('\n')

    # Select test file
    option = 0
    while option > count - 1 or option <1:
        try:
            option = int(input("Please choose an option and press enter: "))
        except ValueError:
            print('Please choose a valid option')
            option = 0
            continue
        if option > count -1 or option < 1:
            print("Please choose a valid option")
    
    file = AvailableTests[option - 1]

    test_words = []
    with open(file, "r") as f:
        for line in f:
            test_words.extend(line.split())    
    
    print('\nThese are the words contained in the selected file:\n')
    display_words(test_words)
    while True:
        confirmfile = input("\nIs this the file you'd like to load (y/n)? ")
        if confirmfile.lower() == 'y':
            main_menu(test_words)
        elif confirmfile.lower() == 'n':
            read_words()

    return test_words

def take_test(fulltest,testwords,test_type):
    """Accepts a list of words and tests spellings"""
    answers = []
    wrong_answers = []
    question_count = 1
    score = 0
    total_questions = len(testwords)
    clear()
    if test_type == 'random':
        random.shuffle(testwords)
    print('You are taking a', test_type, 'test - Good luck!\n')
    print('To hear a word repeated type * and press enter\n')
    for word in testwords:
        print('\nQuestion', question_count, 'of', total_questions)
        answer = '*'
        while answer == '*':
            say(word)
            answer = input('Please type out the spelling of the word and press enter: ')
        question_count += 1
        answers.append(answer.lower())
        if answer.lower() == word:
            score += 1
        else:
            wrong_answers.append(word)
    #Display results at the end of the test
    clear()
    print('********************')
    print('*                  *')
    print('*  Your results!   *')
    print('*                  *')
    print('********************\n')
    for x in range(len(testwords)):
        if answers[x] == testwords[x]:
            print(x+1, answers[x], u'\u2713') 
        else:
            print(x+1, answers[x], 'X\t', testwords[x])
    print('\nYou scored', score, 'out of', len(testwords))
    if score == len(testwords):
        print('You got them all right, well done!')
        input('\nPress enter to go back to the main menu\n')
        main_menu(fulltest)
    else:
        retest = ''
        while True:
            retest = input("\nWould you like retest on the words you got wrong (y/n)? ")
            if retest.lower() == 'y':
                take_test(testwords,wrong_answers, test_type)
            elif retest == 'n':
                main_menu(fulltest)

def select_words(testwords, test_type):
    """Accepts a list of test words and a test_type
    Allows the user to select which words to include
    in the test and then launches a test of 
    the specified type"""
    clear()
    selected_words=[]
    print("Please select the words to include in the test")
    count = 1
    for word in testwords:
        print(str(count)+'.',word)
        count += 1
    print("\nWhen you have finished choosing words enter the number 0.")
    selected = 1
    while selected != 0:
        try:
            selected = int(input("Please enter the number for the word you'd like to include:"))
        except ValueError:
            print('Please choose a valid option')
            continue
        if selected > len(testwords) or selected < 0:
            print('Please choose a vaild option')
        elif selected == 0:
            pass
        else:
            selected_words.append(testwords[selected-1])
    if len(selected_words) == 0:
        input("\nNo words chosen, press enter to return to the main menu\n")
        main_menu(testwords)
    else:
        print('\nYou have chosen to be tested on the following words:')
        for word in selected_words:
            print(word)
        input('\nPress enter to begin the test with the selected words\n')
        take_test(testwords,selected_words,test_type)

def display_words(test_words):
    """Display the test words from testwords.txt"""
    count = 1
    for word in test_words:
        print(str(count)+'.',word)
        count += 1
    return test_words
    

def main_menu(test_words):
    """Displays the main menu and accepts options"""
    #Clear the screen and display the menu
    clear()
    print("------------------------------------")
    print("|                                  |")
    print("|   Spelling Tests for Monsters!   |")
    print("|                                  |")
    print("|            by Dadda              |")
    print("|                                  |")
    print("------------------------------------")
    print("\n\nMain Menu:\n")
    print("1. Take a full test")
    print("2. Take a full test in random order")
    print("3. Run a test of selected words")
    print("4. Run a test of selected words in random order")
    print("5. Display test words")
    print("6. Change test file")
    print("7. Quit Spelling Tests for Monsters\n")
    #Take input and ensure a valid value is entered
    option = 0
    while option >7 or option <1:
        try:
            option = int(input("Please choose an option and press enter: "))
        except ValueError:
            print('Please choose a valid option')
            option = 0
            continue
        if option > 7 or option < 1:
            print("Please choose a valid option")
    #Call the relevant function for the option chosen
    if option == 1:
        take_test(test_words,test_words,'standard')
    elif option == 2:
        take_test(test_words,test_words,'random')
    elif option == 3:
        select_words(test_words,'standard')
    elif option == 4:
        select_words(test_words,'random')
    elif option == 5:
        clear()
        print("The following words are in your spelling test:\n")
        display_words(test_words)
        input('\nPress enter to continue\n')
        main_menu(test_words)
    elif option == 6:
        main_menu(read_words())
    else:
        say('Goodbye')
        quit()


def main():
    say("Welcome to spelling tests for monsters")
    test_words = read_words()
    main_menu(test_words)

main()
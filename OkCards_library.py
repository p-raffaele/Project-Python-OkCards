'''
Library of OkCards, it contains all the functions that are used in the main file
'''
#external libraries
from ast import Delete
from genericpath import exists
import string
from colorama import Style, Fore
from random import randint
from importlib_metadata import version
import pause
from os.path import exists
import os,sys
from platformdirs import user_cache_dir
from sqlalchemy import delete

Version = '1.0'
Author = 'Raffaele Palumbo'

def manipulate_file(fileName):
   print(Fore.LIGHTBLUE_EX, end = '')
   commands = ['/viewfile','/changetheme','/addcards','/deletefile','/commands','/exit']
   command_descriptions = ['- Display the .txt file completely.', '- Change the theme of the file(or description).',
   '- Add new cards to the deck. (quick /a)','- Delete the current file, you cannot restore it!' , 
   '- Show the commands panel.' , 
   '- Return to the previous menu.']
   print(Fore.LIGHTGREEN_EX + 'File loaded successfully.' + Fore.LIGHTBLUE_EX)
   print('[OkCards - Edit Mode]:What do you want to do?')
   print('Current file => ' + Fore.LIGHTYELLOW_EX + fileName)
   print(Fore.LIGHTBLUE_EX, end = '')
   for i in range(len(commands)):
      if i == 2:
         print(Fore.LIGHTYELLOW_EX + '\t' + commands[i] + ' ', end = '')
         print(command_descriptions[i] + Fore.LIGHTBLUE_EX)
      else:
         print('\t' + commands[i] + ' ', end = '')
         print(command_descriptions[i])
   userInput = input('What would you like to do:')
   while userInput != commands[-1]:
      if userInput == commands[0]: #/view
         with open(fileName) as file:
            print(file.read())
      if userInput == commands[1]: #/changetheme
         with open(fileName) as file:
            lines = file.readlines()
            newTheme = input('Enter a theme for the deck stored in ' + fileName + ':')
            lines[1] = 'Theme: ' +  newTheme + '\n'
            print(Fore.LIGHTGREEN_EX, 'The deck was succesfully updated.')
            print(Style.RESET_ALL, end = '')
         with open(fileName,'w') as file:
            for line in lines:
               file.write(line)
      if userInput == commands[2] or userInput == '/a': #/addcards
         with open(fileName) as file:
            print('Ok!You are now editing the file ' + fileName + ' decks')
            print('\t' + '-Enter /showdeck1 to see the first deck.')
            print('\t' + '-Enter /showdeck2 to see the second deck.')
            print('\t' + '-Enter /check [on|off] to turn on/off the check when a new card is entered.')            
            print('\t' + '-Enter /save to exit and save all the decks.')
            print('\t' + '-Enter /exit to close this menu.')
            print('Or just enter the new card.')
            new_commands = ['/showdeck1','/showdeck2','/check on','/check off','/deletecard','/f_delete card','f_delete deck','/save','/exit']
            deck1 = []
            deck2 = []
            checks = 1 #enabled
            userCard = input('Enter the first card:')
            #if userCard != '/showdeck1' and userCard not in commands:
            if userCard not in new_commands:
               user_choose = input('Do you want to save this card: [' + userCard + ']? (enter "no" to cancel, or press any key to confirm.):\n')
               if user_choose.lower() == 'no':
                  print('Ok! This card was throwed away.')
               else:
                  deck1.append(userCard)
                  cardSignificance = input('Enter the signifance:')  
                  user_choose = input('Are you sure the significance is: [' + cardSignificance +'] (enter "no" to cancel, or enter any key.):\n') 
                  while user_choose.lower() == 'no':
                     print('Ok! The significance was discharged.')
                     cardSignificance = input('Enter the significance:')
                     user_choose = input('Are you sure the significance is: [' + cardSignificance +'] (enter "no" to cancel, or enter any key.):\n') 
                  deck2.append(cardSignificance)
            raise_flag = 0
            raise_second_flag = 0
            if userCard == '/showdeck1':  #user may want to check if file has some cards
               #show_current_deck(deck1,deck2,userCard)
               print('Ok! Showing you the first deck now.')   
               print('----------Deck open:')
               print('This is the first time you open the deck, there should not be any entered card.')
               print('You cannot use the command /deletecard yet as there are no cards to delete.')
               a = show_deck(fileName, deck1)
               print('----------Deck closed.')
               raise_flag = 1
               raise_second_flag = 1 
            while userCard != '/save':
               if raise_flag == 0:
                  userCard = input('Enter the next card (or /save to close):')
               if raise_flag == 1:
                  userCard = input('Enter the first card:')
                  raise_flag = 0
               if userCard == '/check off':
                  checks = 0
                  print('Check is now turned off.')
               if userCard == '/check on':
                  checks = 1
                  print('Check is now turned on.')
               if userCard == '/showdeck1' and raise_flag == 0:
                  while userCard != '/exit':
                     print('The following commands are now enabled:')
                     if raise_second_flag != 1:
                        print('\t' + '-Enter /deletecard to delete a card and its meaning.')
                     print('\t' + '-Enter /f_delete [card|deck] to delete a card or deck from the file.')
                     print('\t' + '-Enter /exit to close the deck.')
                     # if raise_flag == 1:
                     #    raise_flag = 0
                     # else:
                     #    #show_current_deck(deck1,deck2,userCard)
                     #    show_deck(fileName, deck1)
                     if userCard == '/f_delete card':
                        force_delete(fileName, userCard)
                     if userCard == '/f_delete deck':
                        force_delete(fileName, userCard)
                     if userCard == '/showdeck1':
                        print('----------Deck open:')
                        show_deck(fileName,deck1)
                        print('----------Deck closed.')
                     if userCard == '/deletecard':
                        if len(deck1) == 0:
                           print('There are no cards to delete, because you have not entered any.')
                        else:
                           print('-----')
                           print('Note:/deletecard will NOT delete the card directly from the deck, always enter /save to save the new state of the deck.')
                           print('Or if you want to remove a card directly from the file, you can use force delete, callable with /f_delete [card|deck].')                          
                           print('You have entered the following cards:')
                           for card in deck1:
                              print('\t -' + card)
                           found = 0
                           cardtodelete = input('Enter the card you want to delete:')
                           for card in range(len(deck1)):
                              if deck1[card] == cardtodelete:
                                 found = 1
                                 index_card = card
                           if found == 1:
                              # for card in range(len(deck2)):
                              #    if card == index_card:
                              #       index_2card = card
                              deck1.pop(index_card)
                              deck2.pop(index_card)
                              #deck2.pop(index_2card)
                              print(Fore.LIGHTGREEN_EX + 'Ok!Card successfully deleted.')
                              print(Style.RESET_ALL, end = '')    
                           else:
                              print(Fore.LIGHTRED_EX + 'Could not find this card in the deck.')
                              print(Style.RESET_ALL, end = '')
                     #if userCard != '/showdeck1' and userCard != '/check off' and userCard != '/check on' and checks == 1:
                     # if userCard not in new_commands:
                     #    user_choose = input('Do you want to save this card: [' + userCard + ']? (enter "no" to cancel, or enter any key.):\n')
                     #    if user_choose.lower() == 'no':
                     #       print('Ok!This card was throwed away.')
                     #    else:
                     #       deck1.append(userCard)
                     userCard = input('Waiting for a command:')
               else:
                  if userCard not in new_commands and raise_flag == 0:
                     #userCard = input('Enter the card:')
                     user_choose = input('Do you want to save this card: [' + userCard + ']? (enter "no" to cancel, or enter any key.):\n')
                     if user_choose.lower() == 'no':
                        print('Ok!This card was throwed away.')
                     else:
                        ###FIX THIS PART
                        deck1.append(userCard)
                        cardSignificance = input('Enter the signifance:')  
                        user_choose = input('Are you sure the significance is: [' + cardSignificance +'] (enter "no" to cancel, or enter any key.):\n') 
                        while user_choose.lower() == 'no':
                           print('Ok!Significance discharged.')
                           cardSignificance = input('Enter the significance:')
                           user_choose = input('Are you sure the significance is: [' + cardSignificance +'] (enter "no" to cancel, or enter any key.):\n') 
                        deck2.append(cardSignificance)
                  raise_flag = 0
               #userCard = input('Enter the card:')
               #if userCard != '/showdeck1' and userCard != '/f_delete deck' and checks == 1:
               # if userCard not in new_commands:
               #    user_choose = input('Do you want to save this card: [' + userCard + ']? (enter "no" to cancel, or enter any key to confirm.):\n')
               #    if user_choose.lower() == 'no':
               #       print('Ok!This card was throwed away.')
               #    else:
               #       deck1.append(userCard)
               #       cardSignificance = input('Enter the signifance:')  
               #       user_choose = input('Are you sure the significance is: [' + cardSignificance +'] (enter "no" to cancel, or enter any key.):\n') 
               #       deck2.append(cardSignificance)
               raise_second_flag = 0

            #Dangerous area:
            lines = file.readlines()
            #look for Deck 1
            lines[2] = lines[2].strip('\n')
            lines[3] = lines[3].strip('\n')
            count = 0
            if len(deck1) == 1:
               lines[2] += deck1[0] #of course is just one card.
               lines[2] += ','
            else:
               for card in deck1:
                  lines[2] += card
                  lines[2] += ','
                  count += 1
            # if len(deck1) != 1:
            #    lines[2] = lines[2].rstrip(',')
            lines[2] += '\n'

            if len(deck1) == 1:
               lines[3] += deck2[0]
               lines[3] += ','
            else:
               for significance in deck2:
                  lines[3] += significance
                  lines[3] += ','
            lines[3] += '\n'

            lines[4] = lines [4].rstrip('\n')
            lines[4] += 'to fix'
            lines[4] += '\n'
            #print(lines) debug purpose
            #rewrite file
         with open(fileName, 'w') as newFile:
             for line in lines:
                newFile.write(line)
         print(Fore.LIGHTGREEN_EX + 'The decks were successfully saved into the file.')
         print(Style.RESET_ALL, end = '')
      if userInput == commands[3]:
         warn = input('Are you sure you want to remove this file? Press any key to confirm, enter "no" to leave:\n')
         if warn.lower() == 'no':
            pass
         else:
            os.remove(fileName)
            print(Fore.LIGHTGREEN_EX + 'The file was successfully removed.')
            graphic()
      if userInput == commands[4]:
         print(Fore.LIGHTBLUE_EX + 'Commands are the following:')
         print('Current file => ' + fileName)
         for i in range(len(commands)):
            print('\t' + commands[i] + ' ', end = '')
            print(command_descriptions[i])
      print('- Enter /exit to close this menu')
      print('- Enter /commands to view all the commands again.')
      userInput = input('What would you like to do:')

def force_delete(fileName, command):
   #user may want to delete one card
   #or the whole deck
      with open(fileName,'r') as file:
         #user remove the whole deck
         #yes I know the solution could be easier than this, with a single line, but I preferred this way
         if command == '/f_delete deck':
            print(Fore.LIGHTYELLOW_EX + 'This will forcibly remove the first and second deck from the file: ' + fileName)
            print(Fore.LIGHTYELLOW_EX + 'You will not be able to backup the decks.')
            print(Fore.LIGHTYELLOW_EX + 'Do you want to continue anyway? yes/no')
            user_choose = input()
            while user_choose != 'yes' and user_choose != 'no':
               user_choose = input(Fore.LIGHTYELLOW_EX + 'Do you want to continue anyway? yes/no\n') 
            list = file.readlines()
            if list[2] == 'Deck 1:\n' and list[3] == 'Deck 2:\n':
               print(Fore.LIGHTYELLOW_EX + 'Decks are already empty!')
               print(Style.RESET_ALL, end = '')
            else:
               list[2] = 'Deck 1:\n'
               list[3] = 'Deck 2:\n'
               with open(fileName, 'w') as file:
                  for line in list:
                     file.write(line)
                  print(Fore.LIGHTGREEN_EX + 'Ok! Deck 1 and Deck 2 were successfully removed.')
                  print(Fore.LIGHTGREEN_EX + fileName + ' is now updated.')
                  print(Style.RESET_ALL, end = '')
         elif command == '/f_delete card':
            lines = file.readlines()
            if lines[2] == 'Deck 1:' and lines[3] == 'Deck 2:':
               print('There are already no cards to remove from the file!')
            else:
               print(Fore.LIGHTYELLOW_EX + 'This will forcibly remove a card from the file.')
               cards = []
               card = ''
               for letter in lines[2]:
                  if letter == ',':
                     cards.append(card)
                  else:
                     card += letter
               cards[0] = cards[0].lstrp('Deck 1:')
               print('The first deck contains the following cards:')
               print(cards)
            

                  


            
            

                  
      


def show_deck(fileName, deck1):
   #not saved yet
   if len(deck1) != 0:
      print('(From OkCards)You have entered the following deck:')
      print('[', end = '')
      for card in deck1:
         if len(deck1) == 1:
            print(card, end = '')
         else:
            print(card, end = ',')
      print(']')
   else:
      print('\n(From OkCards)You have not created any deck yet.')

   #current_deck
   with open(fileName, 'r') as file:
      strings = file.readlines()
      deck1_tmp = str(strings[2])
      deck_tmp = deck1_tmp.strip('\n')
      if deck_tmp == 'Deck 1:':
         print('(From file) ' + fileName + ' has an empty deck!')
         return 1
      else:
         print('(From file)' + fileName + ' has the following deck:')
         print('[', end = '')
         for letter in range(len(deck_tmp)):
            if letter > 6:
               print(deck_tmp[letter], end = '')
         print(']')


def show_current_deck(deck1,deck2,whichone):
   if len(deck1) == 0:
      print('There are no cards in the first deck!')
   elif whichone == '/showdeck1':
      print('----------Deck one:')
      print('Ok! Showing you the first deck now.')
      print('At the moment the first deck has the following cards:')
      for card in deck1:
         print(card)
   elif whichone == '/showdeck2':
      pass
   else:
      pass
         

def create_file():
   print(Fore.LIGHTBLUE_EX, end = '')
   print('[OkCards - Edit Mode]:Enter the name of the file that will store the decks:', end = '')
   fileName = input()
   print(Style.RESET_ALL, end = '')
   try:
      fileName = fileName + '.txt'
      f = open(fileName,'x') #file is created in txt
      f.close()
   finally:
      f = open(fileName,'w')
      line1 = 'OkCards v' + Version + '\n'
      f.write(line1)
      line2 = 'Theme:\n'
      f.write(line2)
      line3 = 'Deck 1:\n'
      f.write(line3)
      line4 = 'Deck 2:\n'
      f.write(line4)
      line5 = 'Number of cards:\n'
      f.write(line5)
      line6 = ''
      for i in range(50):
         line6 += '-'
      f.write(line6)
      f.write('\n!-DO NOT ALTER THIS TXT FILE, ONLY BY /EDIT_MODE -!')
      print(Fore.GREEN + 'Ok!The file was created.')
      input(Fore.LIGHTYELLOW_EX + 'Enter any key to continue...')
      print(Style.RESET_ALL, end = '')
      f.close()
      graphic()

def review(v):
   #messages:
   message_0 = 'Ok!There are no cards that need to be reviewed, congratulation!'
   message_1 = 'Ok! Before the next session begins, let us do a quick recap of the most difficult cards, according to your previous answers.'
   #vars:
   a = []
   track = []
   all_zero = 0
   for z in range(len(v)):
      if v[z] != 0:
         all_zero = 1
         break 
   if all_zero == 0:
      print(message_0)
   else:
      print(message_1)
      #loop that finds the maximum value
      for i in range(len(v)):
         if max(v) != 0:
            a.append(max(v))
            find = 0
            for j in range(len(v)):
               if v[j] == max(v) and find == 0:
                  track.append(j)
                  v[j] = 0
                  find = 1        
   #print(track)
   return track,all_zero

   fileName = input('[Editor]Enter the name of the file that will contain the decks:')
   file = open(fileName)
   print('[Editor]' + fileName,'was successfully created.')

def slow_mode(word):
   #first cycle
   print(Fore.LIGHTBLUE_EX + 'Ok! The word to learn is:', Fore.LIGHTCYAN_EX + word)
   for letter in word:
      print(Style.RESET_ALL, end = '')
      print(Fore.LIGHTBLUE_EX + 'Write the letter you see here:', Fore.LIGHTCYAN_EX +  letter)
      letter_given = input()
      while letter_given != letter:
         print(Fore.LIGHTBLUE_EX + 'Not Ok! The letter you need to write is:', Fore.LIGHTCYAN_EX + letter)
         letter_given = input()
   print(Fore.LIGHTBLUE_EX + 'Ok!You wrote' + Fore.LIGHTCYAN_EX + ' ' +  word)
   
   #second cycle
   print(Fore.LIGHTBLUE_EX + 'Now, you will write this word at least 5 times.')
   for i in range(5):
      word_given = input(Fore.LIGHTCYAN_EX)
      while word_given != word:
         print(Fore.LIGHTBLUE_EX + 'Not Ok! You need to write: ' + Fore.LIGHTCYAN_EX + word)
         word_given = input(Fore.LIGHTCYAN_EX)
   print(Fore.LIGHTBLUE_EX + 'Ok!Get ready, the last learning phase starts in 5 seconds...')
   pause.seconds(5)
   something = ''
   for i in range(20):
      something += '*'
      print(something)
   #third cycle, this learning cycle is special, it will work only under special condition
   print(Fore.LIGHTBLUE_EX + 'Ok! Now a letter was removed from the word, you guess it.')
   print(Fore.LIGHTBLUE_EX + 'Do not scroll up!')
   letter_removed = randint(0, len(word) - 1)
   word_disp = ''
   for i in range(len(word)):
      if i != letter_removed:
         word_disp += word[i]
      else:
         word_disp += '?'
   print(word_disp)
   letter_guessed = input('Your guess is:')
   if letter_guessed != word[letter_removed]:
      print('Not Ok! Wrong guess.')
   else:
      print('Ok! Your guess is correct!')
      
   print(Fore.LIGHTBLUE_EX + 'Ok! The learning phase ends here, now you can read the cards again.')

def graphic():
   print(Fore.LIGHTYELLOW_EX, end = '')
   for i in range(2):
      for k in range(10):
         print('*', end = '')
      if i == 0:
         print('Ok Cards!' + Version, end = '')
   print('')
   print('As simple as Ok.')
   print('Menu:')
   set_commands = ['/start','/create_file','/stop','/edit_mode','/start ']
   print('\t' + '/start - Clean mode, no decks loaded, you will enter the cards.')
   print('\t' + '/start [filename].txt - Load a file, decks will be loaded from it, do please mind the\n\t\t\t\tone space after /start and the file format, or it will raise an error.')
   print('\t' + '/create_file - Create a new file to store the decks.')
   print('\t' + '/edit_mode - *(Experimental mode) edit decks.')
   print('\t' + '/stop - Quit the app.')
   command = input('Your command is:')
   while command not in set_commands and set_commands[4] not in command:
      print('Not Ok! Command is unknown.')
      command = input('Your command is:')
   print(Style.RESET_ALL, end = '')
   while command != set_commands[2]:
      if command == set_commands[0]:
         OkCards()
      if command == set_commands[1]:
         create_file()
      if command == set_commands[3]: 
         fileName = input('Enter the name of the file you want to edit(no need to add .txt):')
         file_exists = exists(fileName + '.txt')
         if file_exists == False:
            print(Fore.LIGHTRED_EX + 'Could not locale the file "' + fileName +'.txt' + '"' + Fore.LIGHTYELLOW_EX)
            print('Do you want to create it? (y/n)')
            userInput = input()
            while userInput != 'y' and userInput != 'n':
               userInput = input('Do you want to create it? (y/n):\n')
            if userInput == 'y':
               create_file()
            else:
               pass
         else:
            manipulate_file(fileName +'.txt')
      if set_commands[4] == '/start ':
         format_command = command
         format_command = format_command.lstrip('/start')
         format_command = format_command.lstrip()
         fileName = format_command
         if fileName == '':
            print(Fore.LIGHTRED_EX + 'Cannot load any file, command is /start [filename].txt')
         elif '.txt' not in fileName:
            print(Fore.LIGHTRED_EX + 'Cannot load this file, format must be .txt')
         elif fileName == '.txt':
            print(Fore.LIGHTRED_EX + 'Cannot load this file, you just entered the format.')
         else:
            deck1, deck2 = load_file(fileName)
            if deck1[0] != 'Null' and deck2[0] != 'Null':
               OkCards(deck1,deck2)
               
      input(Fore.LIGHTYELLOW_EX + 'Enter any key to restart...')
      print(Style.RESET_ALL, end = '')
      graphic()

   print('----------------------')
   print(Fore.LIGHTYELLOW_EX + 'Ok! Thanks for using OkCards v' + Version)
   print('Tought, created, and fully developed by' + Fore.LIGHTBLUE_EX + ' \x1B[3mRaffaele Palumbo\x1B[0m')
   print(Fore.LIGHTYELLOW_EX + '(All rights reserved - please respect the intellectual property).')
   sys.exit() #this is a total deal breaker, it stops the application from running completely.

def load_file(fileName):
   if exists(fileName) == False:
      print(Fore.LIGHTRED_EX + 'This file does not exist!')
      return ['Null'],['Null']
   else:
      file = open(fileName)
      lines = file.readlines()
      file.close()
      print(Fore.LIGHTGREEN_EX + 'The file ' + fileName + ' was successfully loaded.')
      #pause.seconds(1)
      print(Fore.LIGHTYELLOW_EX + '----------')
      print(Fore.LIGHTYELLOW_EX + 'Now loading Deck 1 ...')
      #pause.seconds(0.5)
      #we are sure that the first seven words are reserved for deck 1:
      #and that the last two words are reserved for ,\n
      #hence, we run this solution without calling any string modifier
      deck1_cards = ''
      string_tmp = lines[2]
      for i in range(7,len(string_tmp) - 2):
         deck1_cards += string_tmp[i]
      #is it a smart solution?
      #No I'd say 6.5/10 on a general scale because it chains the user to have a pre-formatted file
      #This solution is highly mathematical, it depends strictly on the format
      #but because textual files read by this app shall not be modified, it works perfectly.
      #hence 9/10 (because there could have been a faster solution)
      #Another solution would be that even though the user may modify the textual file, the app is still able
      #to look independently for a deck in the file, but let us have the freedom to conclude this app.
      #when developing an app, time is an important factor, furthermore a smarter code would
      #go against the app scope, /edit_mode would be essentually useless.
      card = ''
      deck1_cards_list = []
      for letter in deck1_cards:
         if letter == ',':
            deck1_cards_list.append(card)
            card = ''
         else:
            card += letter
      deck1_cards_list.append(card)
      print(Fore.LIGHTGREEN_EX + 'The first deck was loaded successfully!') 
      #pause.seconds(0.5)

      print(Fore.LIGHTYELLOW_EX + 'Now loading Deck 2 ...')
      deck2_cards = ''
      string_tmp = lines[3]
      for i in range(7,len(string_tmp) - 2):
         deck2_cards += string_tmp[i]  
      card = ''
      deck2_cards_list = []
      for letter in deck2_cards:
         if letter == ',':
            deck2_cards_list.append(card)
            card = ''
         else:
            card += letter
      deck2_cards_list.append(card)
      print(Fore.LIGHTGREEN_EX + 'The second deck was loaded successfully!')
      #pause.seconds(0.5)
      return deck1_cards_list, deck2_cards_list
   
#Core function of the game OkCards
def OkCards(d1 = '', d2 = ''):
   print(Fore.LIGHTBLUE_EX, end = '')
   if d1 != '' and d2 != '':
      deck1 = d1
      deck2 = d2
      weights = []
   else:
      deck1 = []
      deck2 = []
      weights = []
      for i in range(10):
         print('-' ,end = '')
      print('Developed by' + Fore.LIGHTCYAN_EX + ' Raffaele Palumbo',end = '')
      print(Style.RESET_ALL, end = '')
      for i in range(10):
         print('-', end = '')
      print('')
      print(Fore.LIGHTBLUE_EX, end = '')
      string_deck1 = input('Welcome!\nCopy & paste the first deck, each card has to be separated with a ",".\n' + Fore.LIGHTCYAN_EX)
      tmp = ''
      for letter in range(len(string_deck1)):
         #print(string_deck1[letter])
         if string_deck1[letter] != ',':
            tmp += string_deck1[letter]
         else: #card is in the deck
            deck1.append(tmp)
            tmp = ''
      #add the last card
      deck1.append(tmp)
      tmp = ''
      print(Fore.LIGHTYELLOW_EX + 'OK!')
      print(Style.RESET_ALL, end = '')

      print(Fore.LIGHTBLUE_EX, end = '')
      string_deck2 = input('\nNow copy & paste the second deck, which should be the meaning of each card given previously, each card has to be separated with a ",".\n' + Fore.LIGHTCYAN_EX)
      for letter in range(len(string_deck2)):
         if string_deck2[letter] != ',':
            tmp += string_deck2[letter]
         else:
            deck2.append(tmp)
            tmp = ''
      deck2.append(tmp)
      tmp = ''
      print(Fore.LIGHTYELLOW_EX + 'OK!')
      print(Style.RESET_ALL, end = '')

   #Verify that both decks have the same lenght
   print(Fore.LIGHTYELLOW_EX, end = '')
   if len(deck1) == len(deck2):
      #game starts
      for i in range(len(deck1)):
         weights.append(0) #generates a list of zeros to keep memory of wrong answers
         
      print(Fore.LIGHTCYAN_EX + 'Deck 1:',deck1)
      print(Fore.LIGHTCYAN_EX + 'Deck 2:',deck2)
      print(Fore.LIGHTBLUE_EX, end = '')
      for i in range(10):
         print('-', end = '')
      print('')
      commands = ['/linear','/casual','/stop']
      print('\t' + '-> Enter "/linear" to show the cards in orderly. (default)')
      print('\t' + '-> Enter "/casual" to show the cards randomly.')
      print('\t' + '-> Enter "/stop" to quit the game')
      print('Note:At the moment only /linear mode will review the difficult cards, /casual mode'
      + ' still does not support the review.')
      print('\t' + '------------------------------------------------------------')
      print(Style.RESET_ALL, end = '')
      user_input = '/linear' #default command
      print(Fore.LIGHTBLUE_EX, end = '')
      while user_input != commands[-1]:
         
         #first mode active /linear, this is default
         if user_input == commands[0]:
            toggle = 1
            while user_input != commands[-1] and toggle == 1:
               no_card = 0
               for card_toGuess in deck1:
                  print('Card:' + Fore.LIGHTCYAN_EX +  '[' + card_toGuess +']')
                  user_input = input(Fore.LIGHTBLUE_EX + 'Your guess:' + Fore.LIGHTCYAN_EX)
                  
                  if user_input == commands[-1]:
                     print(Fore.LIGHTYELLOW_EX + 'Ok! OkCards was successfully closed.')
                     toggle = 0
                     break #kill this loop
                  if user_input == commands[1]:
                     toggle = 2
                     break #kill this loop
                  if user_input.strip() == deck2[no_card].strip() and toggle == 1:
                     print(Fore.LIGHTGREEN_EX + 'Ok! Your answer is correct!')
                     print(Fore.LIGHTBLUE_EX, end = '')
                     print('-------------------')
                  if user_input.strip() != deck2[no_card].strip() and toggle == 1:
                     print(Fore.LIGHTRED_EX + 'Not Ok!Your answer is wrong...')
                     print(Fore.LIGHTBLUE_EX, end = '')
                     #*Answer is shown:
                     print('Remember, the correct answer is:' + Fore.LIGHTCYAN_EX +  deck2[no_card])
                     print(Fore.LIGHTBLUE_EX, end = '')
                     print('-------------------')
                     weights[no_card] += 1
                  no_card += 1
                  
               if toggle == 1:  
                     track,flag = review(weights)
                     if flag == 0:
                        pass
                     else:
                        for diff_index in track:
                           print(Fore.LIGHTRED_EX, end = '')
                           print('*Difficult card*')
                           print('Card:[' + deck1[diff_index] + ']')
                           user_sp_input = input('Your guess:')
                           if user_sp_input.lower() == deck2[diff_index]:
                              print(Fore.LIGHTGREEN_EX + 'Ok! Good job! The answer is correct.')
                           else:
                              print(Fore.LIGHTRED_EX + 'Not Ok! Your answer is still wrong!')
                              #**Answer is shown
                              print('Remember, the correct answer is:', deck2[diff_index])
                           print(Style.RESET_ALL, end = '')
                     print(Fore.LIGHTYELLOW_EX + 'Ok!End of the deck! The game will be restarted soon...\n')
               else: #other toggle values
                  pass
         #second mode is active /casual
         if user_input == commands[1]:
            #this means toggle is also equal to 2
            print('Ok! Now the casual mode is active, cards are shown randomly.')
            #game is runs infinitely unless the user enters /stop or /linear
            #namely, toggle = 0 or toggle = 1
            while toggle != 0 and toggle != 1:
               tmp = randint(0,len(deck1) - 1) #of course deck1 and deck2 are of the sames
               #print(tmp) debug purpose
               print('Card:', deck1[tmp])
               user_input = input('Your guess:')
               if user_input.strip() == commands[-1].strip():
                  print('Ok! OkCards was successfully closed.')
                  toggle = 0
                  break
               if user_input.strip() == commands[1]:
                  pass
               if user_input.strip() == deck2[tmp].strip() and toggle == 2:
                  print('Ok! Your answer is correct!')
               if user_input.strip() != deck2[tmp].strip() and toggle == 2:
                  print('Not Ok! Your answer is wrong!')    
                  #*Answer is shown:
                  print('Remember, the correct answer is', deck2[tmp])
         else:
            pass

   else:
      print('Each deck has a different lenght, there is not a correspondance! Decks are discarded.') 
      print('Size Deck1:', len(deck1))
      print('Size Deck2:', len(deck2))     
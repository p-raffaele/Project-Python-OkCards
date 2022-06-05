from random import randint
from OkCards_library import review

def OkCards():

   deck1 = []
   deck2 = []
   weights = []
   for i in range(10):
      print('-',end = '')
   print('OkCards 1.0',end = '')
   for i in range(10):
      print('-', end = '')
   print('')

   string_deck1 = input('Welcome!\nCopy & paste the first deck, each card has to be separated with a ",".\n')
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
   print('OK!')

   string_deck2 = input('\nNow copy & paste the second deck, which should be the meaning of each card given previously, each card has to be separated with a ",".\n')
   for letter in range(len(string_deck2)):
      if string_deck2[letter] != ',':
         tmp += string_deck2[letter]
      else:
         deck2.append(tmp)
         tmp = ''
   deck2.append(tmp)
   tmp = ''
   print('OK!')

   #Verify that both decks have the same lenght
   if len(deck1) == len(deck2):
      #game starts
      for i in range(len(deck1)):
         weights.append(0) #generates a list of zeros to keep memory of wrong answers
         
      print('Deck 1:',deck1)
      print('Deck 2:',deck2)
      for i in range(10):
         print('-', end = '')
      print('')
      commands = ['/linear','/casual','/stop']
      print('\t' + '-> Enter "/linear" to show the cards in orderly. (default)')
      print('\t' + '-> Enter "/casual" to show the cards randomly.')
      print('\t' + '-> Enter "/stop" to quit the game')
      print('\t' + '------------------------------------------------------------')
      user_input = '/linear' #default command
      while user_input != commands[-1]:
         
         #first mode active /linear, this is default
         if user_input == commands[0]:
            toggle = 1
            while user_input != commands[-1] and toggle == 1:
               no_card = 0
               for card_toGuess in deck1:
                  print('Card: [', card_toGuess +']')
                  user_input = input('Your guess:')
                  
                  if user_input == commands[-1]:
                     print('Ok! OkCards was successfully closed.')
                     toggle = 0
                     break #kill this loop
                  if user_input == commands[1]:
                     toggle = 2
                     break #kill this loop
                  if user_input.strip() == deck2[no_card].strip() and toggle == 1:
                     print('Ok! Your answer is correct!')
                     print('-------------------')
                  if user_input.strip() != deck2[no_card].strip() and toggle == 1:
                     print('Not Ok!Your answer is wrong...')
                     print('-------------------')
                     weights[no_card] += 1
                  no_card += 1
                  
               if toggle == 1:  
                     track,flag = review(weights)
                     if flag == 0:
                        pass
                     else:
                        for diff_index in track:
                           print('*Difficult card*')
                           print('Card: [' + deck1[diff_index] + ']')
                           user_sp_input = input('Your guess:')
                           if user_sp_input.lower() == deck2[diff_index]:
                              print('Ok! Good job! The answer is correct.')
                           else:
                              print('Not Ok! Your answer is still wrong!')
                     print('Ok!End of the deck! The game will be restarted soon...\n')
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
         else:
            pass

   else:
      print('Not OK! Each deck has a different lenght, there is not a correspondance! Decks are discarded.')
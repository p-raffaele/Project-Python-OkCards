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
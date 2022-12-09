#=====================
#INTRODUCTION
#=====================
# A psycholinguistics experiment by Kassaundra Grimes
# Project filename is FinalProject.py 
# This experiment will measure reaction time for the recognition of 3 letter english words versus non words
# This experiment can be used to contrast native versus non-native english speakers reaction times for word recognition

#=====================
#IMPORT MODULES
#=====================
import random
import numpy
import pandas as pd
import os
from psychopy import visual, monitors, core, event, gui
from datetime import datetime

#=====================
#PATH SETTINGS
#=====================
# find current directory
directory = os.getcwd()
print(directory)
# assign a directory to save files to 
path = os.path.join(directory, 'dataFiles')
# if this directory does not exist, make it exist.
if not os.path.exists(path):
   os.makedirs(path)
 # create the filename
filename = ('FinalProjectData.csv')

#=====================
#MONITOR AND WINDOW
#=====================
mon = monitors.Monitor('myMonitor', width=35.56, distance=60)
mon.setSizePix([1920, 1080])
win = visual.Window(fullscr=False, monitor=mon, size=(600,600), color='grey', units='pix')

#=====================
#STIMULUS AND TRIAL SETTINGS
#=====================
# number of blocks and trials
nBlocks = 2
nTrials = 12
totalTrials = nTrials*nBlocks
#=====================
#PREPARE DATA COLLECTION LISTS
#=====================
# empty lists for data collection
words_data = []
accuracies = []
responseTimes = [0]*totalTrials
trialNumbers = [0]*totalTrials
blockNumbers = [0]*totalTrials
nativelanguage = [0]*totalTrials
# fixation cross 
fixation = visual.TextStim(win, text='+', color='black')
# instruction text
instructText = visual.TextStim(win, text='Text will appear on the screen, press W if you recognize it as an English word, press N if it is not a word. Press any key to begin the experiment.')

#=====================
#PREPARE CONDITION LISTS
#=====================
# create 2 lists, one with words and one with non words
words = ['bad','mad','log','rot','rat','wit']
nonwords = ['pgl','kfi','rih','qup','xin','cif']
# list of all the words/nonwords
allwords = words + nonwords

# assign a clock to keep time
trial_timer = core.Clock()

#=====================
#DIALOGUE BOX
#=====================
# create dictionary for dialogue box
exp_info = {'English as a native language?':('Yes','No'), 'Native Languages': '-'}
# create a dialogue box to get information, language can be filled out however participant wants
my_dlg = gui.DlgFromDict(exp_info, title="Language Info")
# add date to the subject info dictionary
date = datetime.now()
exp_info['date'] = str(date.day)+'/'+str(date.month)+'/'+str(date.year)
# add native language response to the list for the dataframe
nativelanguage.append(exp_info['Native Languages'])
# remove one of the zeroes from the list because it's too long for the dataframe
nativelanguage.pop(0)

#=====================
#BLOCK SEQUENCE
#=====================
for iblock in range(nBlocks):
    # set up and show the text in window // then wait for a keypress
    instructText.draw()
    win.flip()
    event.waitKeys()
    # assign a clock to keep time
    trial_timer = core.Clock()
    # counter for iteration in word list
    count = 0
    # random shuffle here so it's different each block
    numpy.random.shuffle(allwords)
    
    #=====================
    #TRIAL SEQUENCE
    #=====================
    for itrial in range(nTrials): 
        # Adding trials and block numbers to data lists
         # overall trial is the current block multiplied by all the trials plus the current trials
        overallTrial = iblock*nTrials+itrial
        # the current block and trial is iblock/itrial is plus one (to compensate for python starting at 0)
        blockNumbers[overallTrial] = iblock+1
        trialNumbers[overallTrial] = itrial+1
        
        # counter for iteration in word list
        if count < 11 :  
            count = count+1
        else :
            count = 0
        # create text stim from word list
        word_text = visual.TextStim(win, text=allwords[count], color = 'black')
        #=====================
        #START TRIAL
        #=====================
        # draw fix and wait
        fixation.draw()
        win.flip()
        core.wait(0.25)
        # reset the timer
        trial_timer.reset()
        #draw text and wait for keypress
        word_text.draw()
        # add the word of the stim to the lists
        words_data.append(word_text.text)
        win.flip()
        # wait for participant to respond
        keys=event.waitKeys(keyList=['w','n'])
         # adding values to lists 
        if keys:
            # add reaction time to the list by getting time from the timer
            responseTimes[overallTrial] = trial_timer.getTime() 
            # add if keypress was accurate or not, compare word text of trial to word vs nonword list
            if str(word_text.text) in words :
                if keys[0] == 'w':
                    accuracies.append('Correct') 
                else:
                    accuracies.append('Incorrect') 
            else:
               if str(word_text.text) in nonwords :
                    if keys[0] == 'n':
                        accuracies.append('Correct') 
                    else:
                        accuracies.append('Incorrect') 
#======================
# END OF EXPERIMENT
#======================         
# create a dataframe by assigning all values from each trial to a dictionary
df = pd.DataFrame(data={
 "Block Number": blockNumbers, 
 "Trial Number": trialNumbers,  
 "Accuracy": accuracies, 
 "Response Time": responseTimes,
 "Words": words_data,
 "Native Languages": nativelanguage
})
# convert the dataframe to a CSV file and save it under the filename (defined earlier) at the data path (also defined earlier)
df.to_csv(os.path.join(path, filename), sep=',', index=False)

# close the window
win.close()
        
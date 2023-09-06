#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import modules 

from psychopy import monitors, visual, event, core, gui
import numpy as np
import random
import pandas as pd
import time
from pathlib import Path


# Create dialogue window to note patient's data

patient_info = {'Patient ID': '','Age': '','Tumor Site' : '','Gender': ''}
dlg = gui.DlgFromDict(patient_info, title='Patient Information')
experiment_directory = Path(r"/Users/lauravavassori/Desktop/attention_task") #define path for saving results

if not dlg.OK:      #quit if cancel is selected
    core.quit()

with open(str(experiment_directory) + '/' +patient_info['Patient ID']+'_attention_task_info.txt', 'w') as f:      #write patient_info to a txt file
    for key, value in patient_info.items():
        f.write(f'{key}: {value}\n')
    

# Set monitor and create window

mon = monitors.Monitor(name='default', width=30, distance=50)
win = visual.Window(size=(1200, 800), fullscr=False, allowGUI=True, color='white', monitor=mon)


# Welcome window, start at keypress

start_message = visual.TextStim(win, text='Press a key to start the trial', color='black', height=0.08)
start_message.draw()
win.flip()


# Initialize variables

shape = ['triangle', 'square']
color = ['blue', 'red']
size = ['big', 'small']
combos = [[sha, col, siz] for sha in shape    #create all possible combinations of items
          for col in color
          for siz in size]

n_blocks = 1 
n_trials = 30
n_stimuli = 5
stimuli_loc = [(-0.6, 0.4), (-0.2, 0.4), (0.2, 0.4), (0.6, 0.4), (0, -0.4)]
n_test_stimuli = 4
n_target_stimuli = 1
big_stimulus_size = (0.30, 0.30)
small_stimulus_size = (0.18, 0.18)
max_presentation_time = 4.0

results = []



# Experiment starts

for block in range (n_blocks):      #loops through the number of blocks
    start_message.draw()
    win.flip()
    event.waitKeys()
    
    for trial in range(n_trials):         #loops through the number of trials
        selected_combos_for_stimuli = random.sample(combos, n_test_stimuli)      #randomic sampling of test stimuli from all combos
        selected_combo_for_target_stimulus = random.sample(combos, n_target_stimuli)     #randomic sampling of target stimulus from all combos so to have both match and no-match trials
        all_stimuli = selected_combos_for_stimuli + selected_combo_for_target_stimulus
        #print(all_stimuli)


        for stimulus_number in range(n_stimuli):            #loops through the number of stimuli
            stimulus_size = big_stimulus_size if (all_stimuli[stimulus_number][2]) == 'big' else small_stimulus_size #assign stimuli features based on their labels
            stimulus_color = (all_stimuli[stimulus_number][1])
            if (all_stimuli[stimulus_number][0]) == 'triangle':
                stimulus = visual.Polygon(win, edges=3, fillColor=stimulus_color, pos=stimuli_loc[stimulus_number], size=stimulus_size) 
            elif (all_stimuli[stimulus_number][0]) == 'square':
                stimulus = visual.Rect(win, fillColor=stimulus_color, pos=stimuli_loc[stimulus_number], size=stimulus_size)    
            stimulus.draw()      

        presentation_time = time.time()    #set the time at which the stimuli are presented, just before 'flip'
        win.flip()
        response = event.waitKeys(keyList=['y', 'n'], maxWait=max_presentation_time)        #response collected via keybord
        response_time = time.time()     #set the time at which response is given

        if selected_combo_for_target_stimulus[0] in selected_combos_for_stimuli:     #define the case in which answer is corretc
            is_correct = 'y'
        else:
            is_correct = 'n'

        accuracy = 0
        
        if response:       #allows to note when response is not given
            if response[0] == is_correct:        #evaluates if the correct response and the response given actually match
                accuracy = 1
                
        reaction_time = response_time - presentation_time       #calculates RT as the time period between stimuli presentation and amswer given

        results.append({'Block': block + 1, 'Trial': trial + 1, 'Response': response[0] if response else None, 'Accuracy': accuracy, 'ReactionTime': reaction_time})    #append to a list the results

        win.flip()
        core.wait(0.5)      #blank screen between trials

      

results_df = pd.DataFrame(results)       #creates dataframe with the results
results_df.to_excel(str(experiment_directory) + '/' + patient_info['Patient ID'] + '_attention_scores.xlsx', index=False)        #converts dataframe to excel file

win.close()
core.quit()


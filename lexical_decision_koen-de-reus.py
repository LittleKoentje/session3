from psychopy import visual, sound, event, core
import pandas as pd
import numpy as np

# Option 1: Lexical decision task

# In a lexical decision task, the participant is presented with a word for a given period of time,
# and asked to respond whether they think it is a real word (or not). Typically, participants will
# respond faster to high-frequency words than to low-frequency words. We are going to build an experiment
# that can do this. You can use the stimuli you created for session 2b (HF/LF/NW); but if you did not
# manage to create the stimuli, or do not like the result, all the stimuli are also in the repository of session 3.
# We have high frequency, low frequency, and non-word stimuli. For the first version, we will make a demo that
# presents a couple of auditory stimuli regardless of the condition. After making an experiment that can simply
# present auditory stimuli and record the response, you can think of a way to neatly randomize the three conditions.

# Key elements of the experiment:
# -        Read the csv with stimulus information
# -        Present an auditory stimulus
# -        Fixation cross-screen
# -        Decision screen
# -        Clock
# -        Keys to press
# -        Record the response & timing

# In a later version, we will include visual stimuli as well, so we can try to see if there is a difference
# in the frequency effect between modalities.

stimuli = pd.read_csv('/Users/koendereus/Desktop/session3/lexical_decision_stimuli.csv')
root = '/Users/koendereus/Desktop/session3/sounds/'

# Change the non-word condition name
stimuli['freq_category'] = stimuli['freq_category'].replace(['none'], 'NW')

# Make a list of all the paths where to find the recordings
recording_paths = []
for i in range(len(stimuli)):
    recording_path = root + stimuli['freq_category'][i] + '/' + stimuli['word'][i]
    recording_paths.append(recording_path)

# Randomise the list of recording paths
recordings = np.random.permutation(recording_paths)

# Set the window and screen fixation element
window = visual.Window((800, 600), color = (1, 1, 1))
fixation = visual.TextStim(window, text = '+', color = (-1, -1, -1))

results = []
for recording in recordings:
    # Load the right audio file
    audio = sound.Sound(recording)

    # Show the trials
    fixation.draw()
    window.flip()
    core.wait(0.5)

    audio.play()
    window.flip()

    # Wait for user input
    clock = core.Clock()
    keys = event.waitKeys(maxWait = 3, keyList = ['z', 'm'], timeStamped = clock)
    if keys is not None:
        key, reaction_time = keys[0]
    else:
        key = None
        reaction_time = 3

    # Store results in a dictionary
    results.append({
        'sound': recording,
        'key': key,
        'reaction_time': reaction_time
    })

# Store results to dataframe and save to CSV
results = pd.DataFrame(results)
results.to_csv('results.csv')
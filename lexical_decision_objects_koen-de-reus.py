from psychopy import visual, sound, event, core
import pandas as pd
import numpy as np

class Experiment:
    def __init__(self, window_size, text_color, background_color):
        self.text_color = text_color
        self.window = visual.Window(window_size, color=background_color)
        self.fixation = visual.TextStim(self.window, text='+', color=text_color)
        self.clock = core.Clock()

    def show_message(self, message):
        stimulus = visual.TextStim(self.window, text=message, color=self.text_color)
        stimulus.draw()
        self.window.flip()
        event.waitKeys()

class AuditoryTrial:
    def __init__(self, experiment, name, audio, fixation_time = 0.5, max_key_wait = 5, keys = ['z', 'm']):
        self.experiment = experiment
        self.name = name
        self.audio = audio
        self.fixation_time = fixation_time
        self.max_key_wait = max_key_wait
        self.keys = keys

    def run(self):
        # Show the trials
        self.experiment.fixation.draw()
        self.experiment.window.flip()
        core.wait(self.fixation_time)

        self.audio.play()
        self.experiment.window.flip()

        # Wait for user input
        start_time = self.experiment.clock.getTime()
        keys = event.waitKeys(maxWait = self.max_key_wait, keyList = self.keys, timeStamped = self.experiment.clock, clearEvents=True)
        if keys is not None:
            key, end_time = keys[0]
        else: # If no keys were pressed
            key = None
            end_time = self.experiment.clock.getTime()

        # Store results in a dictionary
        return {
            'trial': self.name,
            'key': key,
            'start_time': start_time,
            'end_time': end_time
        }

experiment = Experiment((800, 600), (-1, -1, -1), (1, 1, 1))

# Lexical decision task with auditory stimuli
root = '/Users/koendereus/Desktop/session3/sounds/'
stimuli = pd.read_csv('/Users/koendereus/Desktop/session3/lexical_decision_stimuli.csv')

# Change the non-word condition name of the loaded CSV file
stimuli['freq_category'] = stimuli['freq_category'].replace(['none'], 'NW')

# Prepare the different experimental trials
trials = []
for i in range(len(stimuli)):
    audio = sound.Sound(root + stimuli['freq_category'][i] + '/' + stimuli['word'][i])
    trial = AuditoryTrial(experiment, stimuli['freq_category'][i] + '/' + stimuli['word'][i] + '_audio', audio)
    trials.append(trial)

# Randomise the list of trials
trials = np.random.permutation(trials)

# This is a very simple reaction-time experiment, that simply asks you to respond
# as quickly as possible after an auditory stimulus has been presented.
# It is simply a mock experiment to show you how it works.
experiment.show_message('You will be presented a series of sounds, press z or m as quickly as possible after a sound is presented. Press any key to start the experiment.')

results = []
for trial in trials:
    result = trial.run()
    results.append(result)

# Store results to dataframe and save to CSV
results = pd.DataFrame(results)
results['reaction_time'] = results['end_time'] - results['start_time'] # Calculate all the reaction times
results.to_csv('results.csv')
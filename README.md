# Automatic Music Transcription:
# Introduction:
This task deals with detecting the frequencies and onset times of all musical notes (specifically notes produced by a piano) in .mp3 files. This task will attempt to detect a combination of single notes being played and overlapping notes being played simultaneously.
# Dataset:
The dataset used to train and test outcomes will be recordings from the MAPS database. The MAPS database can be found [**here**](
http://www.tsi.telecom-paristech.fr/aao/en/2010/07/08/maps-database-a-piano-database-for-multipitch-estimation-and-automatic-transcription-of-music/).
# Purpose:
The solution to this task can be very valuable for a few reasons:
* Personal Use - for people who want to learn to play a piece of music.
* Academic Use - for people who want to study the features of music.
* Data Use - for generating new data in a form that can be used for training a machine to generate music.

# Input Representation:
Each time unit of the processed recording is represented as a 396 feature long vector, which is made of 4 batches of 99 bins, each representing the intensity of the frequency at that bin, where each bin is a musical note.
The recording is split into 2 overlapping frames with frame lengths of 2048 and 8192 samples.
For each of these frame lengths another set of features accounts for the difference of frquencies of a few previous points.
These each individually have 99 features, so 99*4=396 which accounts for all the features of the a single time unit.

# Output Representation:
I have considered 3 methods of representing the outputs of the system
1. An 88 feature vector representing the probability of that note being played (method 1)
2. An 88 feature vector representing the probability of that note being played, and 1 feature indicating if a note is being played (method 2).
3. An 88 feature vector represnting the probablility of that note being played, and a one-hot encoding indication the probability of the number of notes being played (method 3).

These different methods will provide different methods of determining the number of notes being played. In methods 1 and 2 a threshold will need to be used for the probabilities to determine the notes played, while in method 3 the NN will learn the number of notes and the most likely number of notes will be determined, then those most likely notes will be selected as the predicton.

# Metrics:
6 metrics will be used to compare these 3 output methods.
* General Accuracy - How well the system can predict the notes played at any instance.
* Empty Accuracy - How well the system can predict those instances when no notes are played.
* Non-Empty Accuracy - How well the system can predict the notes played when notes are played
* Number of Notes Accuracy - How well the system can predict the number of notes being played.
* Same Number Note Accuracy - How well the system can predict the notes when the number of notes was correctly predicted.
* Number of Correct Notes Accuracy - How well the system can predict the number out notes out of the number predicted
For single note recognition the last 3 metrics are not relevant.


# SNN:
## Single Notes:
It should be noted that in this case method 2 and method 3 are similar as they tell only if a note is played or not, as those are the only two trained options.
### Method 1:
Here a currently arbitrary threshold of 0.4 is used to determine the note played.

General Accuracy: 0.77
Empty Accuracy: 0.34
Non Empty Accuracy: 0.85

### Method 2:

General Accuracy: 0.82
Empty Accuracy: 0.70
Non Empty Accuracy: 0.83

### Method 3:
General Accuracy: 0.81
Empty Accuracy: 0.81
Non Empty Accuracy: 0.81

## Multiple Notes:
### Method 1:
Here a currently arbitrary threshold of 0.2 is used to determine the note played.

General Accuracy: 0.42
Empty Accuracy: 0.51
Non Empty Accuracy: 0.41
Number of Notes Accuracy: 0.51
Same Number Note Accuracy: 0.82
Number of Correct Notes Accuracy: 0.65


### Method 2:

General Accuracy: 0.49
Empty Accuracy: 0.79
Non Empty Accuracy: 0.46
Number of Notes Accuracy: 0.57
Same Number Note Accuracy: 0.85
Number of Correct Notes Accuracy: 0.80

### Method 3:
General Accuracy: 0.54
Empty Accuracy: 0.79
Non Empty Accuracy: 0.52
Number of Notes Accuracy: 0.68
Same Number Note Accuracy: 0.79
Number of Correct Notes Accuracy: 0.72

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

# Preprocessing:
Each time unit of the processed recording is represented as a 396 feature long vector, which is made of 4 batches of 99 bins, each representing the intensity of the frequency at that bin, where each bin is a musical note.
The recording is split into 2 overlapping frames with frame lengths of 2048 and 8192 samples.
For each of these frame lengths another set of features accounts for the difference of frquencies of a few previous points.
These each individually have 99 features, so 99*4=396 which accounts for all the features of the a single time unit.

# Output Representation:
I have considered 3 methods of representing the outputs of the system
* 1. An 88 feature vector representing the probability of that note being played
* 2. An 88 feature vector representing the probability of that note being played, and 1 feature indicating if a note is being played.
3. An 88 feature vector represnting the probablility of that note being played, and a one-hot encoding indication the probability of the number of notes being played.

These different methods will provide different methods of determining the number of notes being played. In methods 1 and 2 a threshold will need to be used for the probabilities to determine the notes played, while in method 3 the NN will learn the number of notes and the most likely number of notes will be determined, then those most likely notes will be selected as the predicton.

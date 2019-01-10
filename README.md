# Automatic Music Transcription:
# Introduction:
This task deals with detecting the frequencies and onset times of all musical notes (specifically notes produced by a piano) in .wav files. This task will attempt to detect a combination of single notes being played and overlapping notes being played simultaneously.

# Instruction for use:
The libraries needed are listed in requirements.txt.</br>
To use this system with your own .wav files you must do the following
1. Generate the training data. This is done by running "Preprocess-Training". You must replace the "dataset_path_wav" and "dataset_path_txt" variables to point to where you have stored the training data and labels.
2. Generate the models. This is done by running "Model". You may wish to change the layer configuration.
3. Process your own recordings. Place those recordings you want transcribed in a folder, and run "Preprocess-Inputs". You must replace "dir_path" with the path to your folder.
4. Generate midi files. This is done by running "Generate". You must replace "dir_path" with the path to your folder.

# Dataset:
The dataset used to train and test outcomes will be recordings from the MAPS database. The MAPS database can be found [**here**](
http://www.tsi.telecom-paristech.fr/aao/en/2010/07/08/maps-database-a-piano-database-for-multipitch-estimation-and-automatic-transcription-of-music/).
# Purpose:
The solution to this task can be very valuable for a few reasons:
* Personal Use - for people who want to learn to play a piece of music.
* Academic Use - for people who want to study the features of music.
* Data Use - for generating new data in a form that can be used for training a machine to generate music.

# Example Outputs:
Mozart's k265 can be found here: [**Original**](https://raw.githubusercontent.com/benjikershenbaum/Automatic-Music-Transcription/master/Examples/Original/MozartK265.wav) </br> My systems output with: </br>
[**1 Layer**](https://github.com/benjikershenbaum/Automatic-Music-Transcription/blob/master/Examples/1%20Layer/out_MozartK265_n.mid?raw=true) </br>
[**2 Layers**](https://github.com/benjikershenbaum/Automatic-Music-Transcription/blob/master/Examples/2%20Layer/out_MozartK265_n.mid?raw=true) </br>
[**3 Layers**](https://github.com/benjikershenbaum/Automatic-Music-Transcription/blob/master/Examples/3%20Layer/out_MozartK265_n.mid?raw=true) </br>
[**4 Layers**](https://github.com/benjikershenbaum/Automatic-Music-Transcription/blob/master/Examples/4%20Layer/out_MozartK265_n.mid?raw=true) </br>

# Input Representation:
The feature extraction of the inputs is done as follows:
1. Calculate the frequency intensity/time matrix using an stft with a hamming window of length 4096 and window length 8192
2. Convert both matracies to a note frequency intesity/time matrix. In other words for each time step calculate the weighted avarage of all the frequency bins that lie in the range of two adjacent notes. This is done up to note 100, where note 1 is A0 - frequency 27.5 and note 100 is of frequency 8372. This is done as the 88th note (C8 - frequency 4186) has a second harmonic at the frequency of note 100 (i.e. octave). This in total is already 200 features for each time step.
3. Calculate the difference between each of the note frequency and its previous time step note frequency. This results in the remaining 200 features
This yields a n x 400 input matrix where n is the number of time steps determined by the 8192 window spectrogram time bins.

# Preprocessing:
To reduce noise in the input histogram I performed histogram equalization, this would reduce the spectrogram from this 
</br>
![alt text](https://raw.githubusercontent.com/benjikershenbaum/Automatic-Music-Transcription/master/Images/Before.png)
</br>
to this 
</br>
![alt text](https://raw.githubusercontent.com/benjikershenbaum/Automatic-Music-Transcription/master/Images/After.png)

# Output Representation:
I have considered 3 methods of representing the outputs of the system
1. An 88 feature vector representing the probability of that note being played (method 1 - m_n)
2. An 88 feature vector representing the probability of that note being played, and 1 feature indicating if a note is being played (method 2 - m_e).
3. An 88 feature vector represnting the probablility of that note being played, and a one-hot encoding indication the probability of the number of notes being played (method 3 - m_h).

These different methods will provide different methods of determining the number of notes being played. In methods 1 and 2 a threshold will need to be used for the probabilities to determine the notes played, while in method 3 the NN will learn the number of notes and the most likely number of notes will be determined, then those most likely notes will be selected as the predicton.

Once the output of probabilites is created we must determine how many notes are being played, and which notes are being played. 
For method 1 and method 2 this is done by first applying an arbitrary threshold value of 0.03. In other words, any note with probability 0.03 or lower is set to 0. Then K-Means clustering is used on the remaining 1D data to try and find the notes which are played (i.e. cluster of higher probabilities). 

For method 3 we simply select the highest probablitiy number of notes being played (n), and the find the n highest note probabilities. 

# Metrics:
6 metrics will be used to compare these 3 output methods.
* General Accuracy - How well the system can predict the notes played at any instance.
* Empty Accuracy - How well the system can predict those instances when no notes are played.
* Non-Empty Accuracy - How well the system can predict the notes played when notes are played
* Number of Notes Accuracy - How well the system can predict the number of notes being played.
* Same Number Note Accuracy - How well the system can predict the notes when the number of notes was correctly predicted.
* Number of Correct Notes Accuracy - How well the system can predict the number out notes out of the number predicted

For testing, the training done with a 80%/20% training/testing split on the data.

# Example Outputs:
Sample outputs for the following sections of music can be found in the Examples folder for each of the varients of the data and neural networks:
1. African Ripples
2. After You've Gone
3. Ain't Misbehavin
4. Being the Beuine
5. Easy Living
6. Fur Elise
7. Mozart K265
8. C Major Scale
9. Viper's Drag

# Future Plans
The next step of this project is to improve the transcription by using Bidirectional LSTM Recurrent Neural Network, which will improve transcription accuracy greatly.
Dimension reduction using clustering and PCA may also be worth investigating

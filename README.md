# Voice-Cloner-assistant

# How it works

The main goal is to return an audio file that contains speech of the given text. The user should be able to :  
1. Select the speaker ID from a list of available IDs.
2. Upload own voice to replicate.
I have used a Bark TTS model to generate the audio using Voice prompting. It intially has a sample rate of 24000. We load the Bark model from a directory. We need to clone the Bark model's checkpoints from it's repository into a directory first before using this app. Store the checkpoints in a directory named 'bark_model'.

Next we intialize it with a basic config. 

We have the following endpoints in the app: 

1. [POST] '/upload-voice'

This method alows a user to send an audio file of his/her own voice to the app. We will read that file and assign a random speaker ID to the file. We will store the file under the directory : 'bark_voices' under the name as it's speaker ID. When the model wants to generate the audio using this file, it will simply search for the ID in the 'bark_voices' directory.

2. [POST] '/generate'

This endpoint is called to generate the speech from the given text. It takes 2 arguments: 'text' (The text to generate the audio from) and 'speaker' (Speaker ID of the voice to generate the audio from). The model with synthesize the audio using these 2 arguments and the endpoint will return an output file ('generated_speech.wav') to the client.

I have added these endpoints in the file 'audioflask2apis.py'.

I have added sample client code in the file 'audioflaskclient.py'.

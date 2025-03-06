import requests

# Test with custom voice
'''
with open('bark_voices/speaker_4/utsav.wav', 'rb') as f:
    response = requests.post(
        'http://127.0.0.1:5000/generate',
        data={'text': 'Hello! This is a test. I am AI engineer'},
        files={'voice_file': f}
    )
'''
response = requests.post('http://127.0.0.1:5000/generate',data={'text': 'Hello! This is a test. I am AI engineer','speaker':'speaker_4'})
if response.status_code == 200:
    with open('clientoutput.wav', 'wb') as f:
        f.write(response.content)
else:
    print(f"Error: {response.json()}")
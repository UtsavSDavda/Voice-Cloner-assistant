from flask import Flask, request, send_file, jsonify
import os
import scipy
from TTS.tts.configs.bark_config import BarkConfig
from TTS.tts.models.bark import Bark
#import threading
import tempfile
import uuid
from werkzeug.utils import secure_filename
#import shutil

config = BarkConfig()
sample_rate = 24000
model = Bark.init_from_config(config=config)
model.load_checkpoint(config, checkpoint_dir="bark_model/bark/",eval=True)        

app = Flask(__name__)

def generate_audio(text, speaker_id=None):
    try:
        if speaker_id and os.path.exists(os.path.join('bark_voices', speaker_id)):
            output_dict = model.synthesize(
                text=text,
                config=config,
                speaker_id=speaker_id,
                voice_dirs=['bark_voices']
            )
        else:
            output_dict = model.synthesize(
                text=text,
                config=config,
                speaker_id="speaker_1",
                voice_dirs=["bark_voices"]
            )

        output_path = os.path.join(tempfile.gettempdir(), f'output_{uuid.uuid4()}.wav')
        scipy.io.wavfile.write(
            output_path,
            rate=sample_rate,
            data=output_dict["wav"]
        )
        return output_path
    except Exception as e:
        raise Exception(f"Error generating audio: {str(e)}")
    
@app.route('/upload-voice', methods=['POST'])
def upload_voice():
    try:
        if 'voice_file' not in request.files:
            return jsonify({'error': 'No voice file provided'}), 400
        
        voice_file = request.files['voice_file']
        if voice_file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        speaker_id = str(uuid.uuid4())[:8]
        voice_dir = os.path.join('bark_voices', speaker_id)
        
        os.makedirs(voice_dir, exist_ok=True)
        
        voice_filename = secure_filename(voice_file.filename)
        voice_path = os.path.join(voice_dir, voice_filename)
        voice_file.save(voice_path)
        
        return jsonify({
            'message': 'Voice uploaded successfully',
            'speaker_id': speaker_id
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/generate',methods=['POST'])
def generate_voice():
    try:
        if 'text' not in request.form:
            return {'error': 'No text provided'}, 400
        if 'speaker' not in request.form:
            return {'error': 'Provide Speaker ID.'}, 400
        
        text = request.form['text']
        speaker_id = request.form.get('speaker')

        output_path = generate_audio(text, speaker_id)
        
        return send_file(
            output_path,
            mimetype='audio/wav',
            as_attachment=True,
            download_name='generated_speech.wav'
        )
    
    except Exception as e:
        return {'error': str(e)}, 500
    
if __name__ == '__main__':
    os.makedirs('bark_voices', exist_ok=True)
    app.run(host='127.0.0.1', port=5000, debug=True)
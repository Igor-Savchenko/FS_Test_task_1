import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['mp3'])

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    for file_name in os.listdir(app.static_folder):
            os.remove(os.path.join(app.static_folder, file_name))
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            origin_filename=file.filename
            filename = secure_filename(file.filename)
            path=os.path.join(app.static_folder, filename)
            file.save(path)
            
            # To work load required to install ffmpeg and add the path to it in the system environment variables
            y, sr = librosa.load(path)
            D = np.abs(librosa.stft(y))
            librosa.display.specshow(librosa.amplitude_to_db(D, ref=np.max),
                                    y_axis='log', x_axis='time')
            plt.title('Power spectrogram')
            plt.colorbar(format='%+2.0f dB')
            plt.tight_layout()
            os.remove(path)
            output_filename=filename.split('.')[0]+'_spectre.svg'
            output_path=os.path.join(app.static_folder, output_filename)
            plt.savefig(output_path)
            plt.clf()
            return render_template('result.html', filename=origin_filename, output_filename=output_filename)

    return render_template('index.html')

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.run(debug=True)
        
    
# Import required packages
import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename

# Set allowed file extensions 
ALLOWED_EXTENSIONS = set(['mp3'])

# Define application
app = Flask(__name__)

def allowed_file(filename):
    '''
    Function get string (filename or path) and return True if the file
    extension are permitted, and False in other cases 
    '''
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# It is single page web-application, only one URL is used
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    '''
    General function of application, upload mp3 audiofile, converts it into a
    SVG spectrum image and show it in browser
    '''
    # Delete unnecessary static files if they exist so as not to clutter up 
    # the server 
    for file_name in os.listdir(app.static_folder):
            os.remove(os.path.join(app.static_folder, file_name))
    # In case of POST request
    if request.method == 'POST':
        
        # Code from:
        # http://flask.pocoo.org/docs/1.0/patterns/fileuploads/

        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also submit an empty part
        # without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        # if user upload file with correct extension
        if file and allowed_file(file.filename):
            origin_filename=file.filename # Need for show filename  in browser
            filename = secure_filename(file.filename)
            path=os.path.join(app.static_folder, filename)
            file.save(path)
            
            # Code from:
            # https://librosa.github.io/librosa/generated/librosa.core.stft.html?highlight=stft

            # For the librosa.load() are working required to install ffmpeg
            # and add the path to it in the system environment variables
            y, sr = librosa.load(path)
            D = np.abs(librosa.stft(y))
            librosa.display.specshow(librosa.amplitude_to_db(D, ref=np.max),
                                    y_axis='log', x_axis='time')
            plt.title('Power spectrogram')
            plt.colorbar(format='%+2.0f dB')
            plt.tight_layout()
            os.remove(path) # Remove audiofile
            output_filename=filename.split('.')[0]+'_spectre.svg'
            output_path=os.path.join(app.static_folder, output_filename)
            plt.savefig(output_path)
            plt.clf() # Clear plt after output
            return render_template('result.html', filename=origin_filename, output_filename=output_filename)

    return render_template('index.html')

# This block only for debug, in production app start from other file 
# (wsgi.py for example)
if __name__ == "__main__":
    # If secret key not define flask gives a warning when 
    # request.files['file'].filename==''
    app.secret_key = 'super secret key'
    app.run(debug=True)
        
    
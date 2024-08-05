import os
from flask import Flask, request, send_from_directory, redirect, url_for, render_template, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Directory where images are stored
IMAGE_DIRECTORY = '/path/to/your/images'  # Update this to your image directory path

# Path to the settings file
SETTINGS_FILE = 'settings.txt'

# Allowed extensions for image uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Check if the uploaded file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Read settings from the settings file
def read_settings():
    settings = {'nextImage': 30, 'refreshImages': 60}  # Default values
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            lines = f.readlines()
            for line in lines:
                key, value = line.strip().split('=')
                settings[key] = int(value)
    return settings

# Write settings to the settings file
def write_settings(next_image, refresh_images):
    with open(SETTINGS_FILE, 'w') as f:
        f.write(f"nextImage={next_image}\n")
        f.write(f"refreshImages={refresh_images}\n")

@app.route('/image/<filename>')
def get_image(filename):
    return send_from_directory(IMAGE_DIRECTORY, filename)

@app.route('/upload', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' in request.files:
            file = request.files['file']
            # If the user does not select a file, the browser submits an empty file without a filename
            if file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(IMAGE_DIRECTORY, filename))
        
        # Handle settings update
        if 'nextImage' in request.form and 'refreshImages' in request.form:
            next_image = request.form.get('nextImage', type=int)
            refresh_images = request.form.get('refreshImages', type=int)
            write_settings(next_image, refresh_images)
        
        return redirect(url_for('upload_image'))

    # List all images in the directory
    images = [img for img in os.listdir(IMAGE_DIRECTORY) if img.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    settings = read_settings()
    return render_template('upload.html', images=images, settings=settings)

@app.route('/delete/<filename>', methods=['POST'])
def delete_image(filename):
    # Delete the image file from the directory
    file_path = os.path.join(IMAGE_DIRECTORY, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    return redirect(url_for('upload_image'))

@app.route('/images', methods=['GET'])
def get_images():
    # List all images in the directory
    images = [img for img in os.listdir(IMAGE_DIRECTORY) if img.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    return jsonify(images)

@app.route('/settings', methods=['GET'])
def get_settings():
    # Return current settings as JSON
    settings = read_settings()
    return jsonify(settings)

@app.route('/')
def index():
    # Render the gallery view with current images and settings
    images = [img for img in os.listdir(IMAGE_DIRECTORY) if img.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    settings = read_settings()
    return render_template('gallery.html', images=images, settings=settings)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4488)

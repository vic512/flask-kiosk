import os
import time
from flask import Flask, request, send_from_directory, redirect, url_for, render_template, jsonify
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)

# Directory where images are stored
IMAGE_DIRECTORY = '/app/images'  # Update this to your image directory path

# Path to the settings file
SETTINGS_FILE = 'settings.txt'

# Allowed extensions for image uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Check if the uploaded file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Read settings from the settings file
def read_settings():
    settings = {'nextImage': 30, 'refreshImages': 60, 'imageWidth': 800, 'imageHeight': 600, 'rotateImages': 0}  # Default values
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            lines = f.readlines()
            for line in lines:
                key, value = line.strip().split('=')
                settings[key] = int(value)
    return settings

# Write settings to the settings file
def write_settings(next_image, refresh_images, image_width, image_height, rotate_images):
    with open(SETTINGS_FILE, 'w') as f:
        f.write(f"nextImage={next_image}\n")
        f.write(f"refreshImages={refresh_images}\n")
        f.write(f"imageWidth={image_width}\n")
        f.write(f"imageHeight={image_height}\n")
        f.write(f"rotateImages={rotate_images}\n")

@app.route('/image/<filename>')
def get_image(filename):
    return send_from_directory(IMAGE_DIRECTORY, filename)

@app.route('/upload', methods=['GET', 'POST'])
def upload_image():
    settings = read_settings()
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' in request.files:
            file = request.files['file']
            # If the user does not select a file, the browser submits an empty file without a filename
            if file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)

                # Create a unique filename by appending a timestamp
                name, ext = os.path.splitext(filename)
                timestamp = int(time.time())
                unique_filename = f"{name}_{timestamp}{ext}"

                # Save the file temporarily to resize it
                temp_path = os.path.join(IMAGE_DIRECTORY, unique_filename)
                file.save(temp_path)

                # Open and resize the image while maintaining aspect ratio
                with Image.open(temp_path) as img:
                    original_width, original_height = img.size
                    target_width, target_height = settings['imageWidth'], settings['imageHeight']

                    # Calculate new dimensions to maintain aspect ratio
                    aspect_ratio = original_width / original_height
                    if (target_width / target_height) > aspect_ratio:
                        new_height = target_height
                        new_width = int(new_height * aspect_ratio)
                    else:
                        new_width = target_width
                        new_height = int(new_width / aspect_ratio)

                    img = img.resize((new_width, new_height), Image.LANCZOS)
                    img.save(temp_path)

        # Handle settings update
        if all(k in request.form for k in ['nextImage', 'refreshImages', 'imageWidth', 'imageHeight', 'rotateImages']):
            next_image = request.form.get('nextImage', type=int)
            refresh_images = request.form.get('refreshImages', type=int)
            image_width = request.form.get('imageWidth', type=int)
            image_height = request.form.get('imageHeight', type=int)
            rotate_images = request.form.get('rotateImages', type=int)
            write_settings(next_image, refresh_images, image_width, image_height, rotate_images)
        
        return redirect(url_for('upload_image'))

    # List all images in the directory
    images = [img for img in os.listdir(IMAGE_DIRECTORY) if img.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
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
    app.run(debug=True, host='0.0.0.0', port=4444)

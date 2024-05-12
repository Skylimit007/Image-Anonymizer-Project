from flask import Flask, request, send_file
from PIL import Image, ImageOps
import io

app = Flask(__name__)

@app.route('/')
def index():
    return send_file('templates/index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return 'No image uploaded', 400

    image_file = request.files['image']
    if image_file.filename == '':
        return 'No selected image', 400

    try:
        image = Image.open(image_file)

        # Remove metadata and apply Exif orientation correction
        image_without_exif = ImageOps.exif_transpose(image)

        # Save cleaned image to a temporary in-memory file
        output = io.BytesIO()
        image_without_exif.save(output, format=image.format)
        output.seek(0)

        return send_file(output, mimetype='image/' + image.format, as_attachment=True, download_name=image_file.filename)
    except Exception as e:
        print(str(e))
        return 'Failed to process image', 500

if __name__ == '__main__':
    app.run(debug=True)

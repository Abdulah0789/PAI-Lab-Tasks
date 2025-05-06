from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os
from caption_generator import generate_caption

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['image']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            caption = generate_caption(filepath)

            web_path = filepath.replace("\\", "/")

            return render_template('result.html', image_path=web_path, caption=caption)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

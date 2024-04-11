from flask import Blueprint, request, current_app, jsonify
from werkzeug.utils import secure_filename
from application.models.models import db, Task
import os
from datetime import datetime

video_blueprint = Blueprint('video', __name__)

@video_blueprint.route('/tasks', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']
    filename = secure_filename(file.filename)
    
    now = datetime.now()
    year, month, day = now.strftime("%Y"), now.strftime("%m"), now.strftime("%d")
    
    directory_path = os.path.join(current_app.config['UPLOAD_FOLDER'], year, month, day)
    
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    filepath = os.path.join(directory_path, filename)
    file.save(filepath)

    new_task = Task(status='uploaded')
    db.session.add(new_task)
    db.session.commit()

    return jsonify({'message': f'Video {filename} subido', 'task_id': new_task.id}), 201
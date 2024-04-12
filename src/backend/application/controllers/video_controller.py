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
    
    project_root = current_app.root_path
    directory_path = os.path.join(project_root, current_app.config['UPLOAD_FOLDER'], year, month, day)
    video_path = os.path.join(year, month, day, filename)
    
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    filepath = os.path.join(directory_path, filename)
    file.save(filepath)
    
    user_id = 1

    new_task = Task(user_id=user_id, status='uploaded', file_path=video_path)
    db.session.add(new_task)
    db.session.commit()

    #TODO enviar mensaje a rabbit con contenido igual al nombre del video siguiendo la logica del send.py en carpeta broker 


    return jsonify({'message': f'Video {os.path.join(directory_path, filename)} uploaded', 'task_id': new_task.id}), 201


@video_blueprint.route('/tasks', methods=['GET'])
def get_tasks():
    print("get tasks")
    # Query users from the database using SQLAlchemy
    tasks = Task.query.all()
    # Serialize users to JSON
    if not tasks:
        return jsonify({'data': "no entries"}), 200

    tasks_list = [{'id': task.id, 'status': task.status} for task in tasks]
    return jsonify({'data': tasks_list}), 200


@video_blueprint.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return jsonify({'message': 'Task not found'}), 404

    file_path = task.file_path
    
    project_root = current_app.root_path
    video_sin_editar = os.path.join(project_root, current_app.config['UPLOAD_FOLDER'], file_path)
    video_editado = os.path.join(project_root, current_app.config['UPLOAD_FOLDER_EDIT'], file_path)
    
    if os.path.exists(video_sin_editar):
        os.remove(video_sin_editar)
    if os.path.exists(video_editado):
        os.remove(video_editado)

    db.session.delete(task)
    db.session.commit()

    return jsonify({'message': 'Eliminado', 'file': f'{file_path}', 'Task': task_id}), 200

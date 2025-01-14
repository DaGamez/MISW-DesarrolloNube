from flask import Blueprint, jsonify, send_file


video_download_blueprint = Blueprint('video_download', __name__)


@video_download_blueprint.route('/video/test/download/<string:video_name>', methods=['GET'])
def test_download_video(video_name):
    try:
        if video_name == '':
            return jsonify({'message': 'El nombre del video no puede estar vacío.'}), 400
        
        if video_name is None:
            return jsonify({'message': 'El nombre del video no puede ser nulo.'}), 400
        
        if video_name == 'undefined':
            return jsonify({'message': 'El nombre del video no puede ser indefinido.'}), 400
        
        if video_name == 'null':
            return jsonify({'message': 'El nombre del video no puede ser nulo.'}), 400
        
        if video_name.endswith(".mp4"):
            video_name = video_name[:-4]
        
        filename = '/usr/src/app/application/controllers/video_test/'+str(video_name)+'.mp4'

        try:
            with open(filename, 'r') as file:
                pass
        except FileNotFoundError:
            return jsonify({
                'message': 'El video solicitado no se encuentra en el servidor. Por favor, verifique el nombre de su video e intente nuevamente.',
                'error': str(e)
            }), 500
        
        return send_file(filename, as_attachment=True)
    
    except Exception as e:
        return jsonify({
            'message': 'Ha ocurrido un error al descargar el video. Por favor, intente nuevamente.',
            'error': str(e)
        }), 500
    

@video_download_blueprint.route('/video/download/<int:ano>/<int:mes>/<int:dia>/<string:video_name>', methods=['GET'])
def download_video(ano, mes, dia, video_name):
    try:
        if video_name == '':
            return jsonify({'message': 'El nombre del video no puede estar vacío.'}), 400
        
        if video_name is None:
            return jsonify({'message': 'El nombre del video no puede ser nulo.'}), 400
        
        if video_name == 'undefined':
            return jsonify({'message': 'El nombre del video no puede ser indefinido.'}), 400
        
        if video_name == 'null':
            return jsonify({'message': 'El nombre del video no puede ser nulo.'}), 400
        
        if video_name.endswith(".mp4"):
            video_name = video_name[:-4]

        month = str(mes).zfill(2)
        filename = '/usr/src/app/uploads/videos_editados/'+str(ano)+'/'+str(month)+'/'+str(dia)+'/'+str(video_name)+'.mp4'

        try:
            with open(filename, 'r') as file:
                pass
        except FileNotFoundError as e:
            return jsonify({
                'message': 'El video solicitado no se encuentra en el servidor. Por favor, verifique el nombre de su video e intente nuevamente.',
                'error': str(e)
            }), 500

        return send_file(filename, as_attachment=True)
    
    except Exception as e:
        return jsonify({
            'message': 'Ha ocurrido un error al descargar el video. Por favor, verifique el nombre de su video e intente nuevamente.',
            'error': str(e)
        }), 500
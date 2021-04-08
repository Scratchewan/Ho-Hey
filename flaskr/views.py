from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import database
import json
# import numpy as np
# import cv2
import base64
import tensorflow as tf
import pickle

views = Blueprint('views', __name__)

init_Base64 = 21
label_dict = {0: 'Cat', 1: 'Giraffe', 2: 'Sheep',
              3: 'Bat', 4: 'Octopus', 5: 'Camel'}
graph = tf.get_default_graph()

with open(f'flaskr\model_cnn.pkl', 'rb') as f:
    model = pickle.load(f)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            database.session.add(new_note)
            database.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            database.session.delete(note)
            database.session.commit()

    return jsonify({})


@views.route('/pen')
def pen():
    return render_template("pen.html", user=current_user)


@views.route('/draw')
def draw():
    return render_template('draw.html')


@views.route('/predict', methods=['POST'])
def predict():
    global graph
    with graph.as_default():
        if request.method == 'POST':
            final_pred = None
            draw = request.form['url']
            draw = draw[init_Base64:]
            # draw_decoded = base64.b64decode(draw)
            # image = np.asarray(bytearray(draw_decoded), dtype="uint8")
            # image = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)
            # resized = cv2.resize(image, (28, 28), interpolation=cv2.INTER_AREA)
            # vect = np.asarray(resized, dtype="uint8")
            # vect = vect.reshape(1, 1, 28, 28).astype('float32')
            # my_prediction = model.predict(vect)
            # index = np.argmax(my_prediction[0])
            # final_pred = label_dict[index]

    return render_template('results.html', prediction=final_pred)

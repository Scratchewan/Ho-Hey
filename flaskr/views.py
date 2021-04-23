from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import database
import json
import numpy as np
import cv2
import base64
import tensorflow as tf
import pickle
import os
# from PIL import Image

views = Blueprint('views', __name__)

init_Base64 = 21
label_dict = {0: 'Cat', 1: 'Giraffe', 2: 'Sheep',
              3: 'Bat', 4: 'Octopus', 5: 'Camel'}
graph = tf.get_default_graph()

enviroment = 'production'

if enviroment == 'development':
    path = f'flaskr\model_cnn.pkl'
elif enviroment == 'production':
    path = f'/app/flaskr/model_cnn.pkl'

with open(path, 'rb') as f:
    model = pickle.load(f)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
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


@views.route('/predict', methods=['POST'])
def predict():
    global graph
    with graph.as_default():
        if request.method == 'POST':
            final_pred = None
            draw = request.form['url']
            draw = draw[init_Base64:]
            draw_decoded = base64.b64decode(draw)
            image = np.asarray(bytearray(draw_decoded), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)
            resized = cv2.resize(image, (28, 28), interpolation=cv2.INTER_AREA)
            vect = np.asarray(resized, dtype="uint8")
            vect = vect.reshape(1, 1, 28, 28).astype('float32')
            my_prediction = model.predict(vect)
            index = np.argmax(my_prediction[0])
            final_pred = label_dict[index]

    return render_template('results.html', prediction=final_pred, user=current_user)


@views.route('/draw', methods=['POST'])
def draw():
    if request.method == 'POST':
        if request.form.get('dict') == "Cat":
            dict = "gato"
        elif request.form.get('dict') == "Giraffe":
            dict = "girafa"
        elif request.form.get('dict') == "Sheep":
            dict = "ovelha"
        elif request.form.get('dict') == "Bat":
            dict = "morcego"
        elif request.form.get('dict') == "Octopus":
            dict = "polvo"
        elif request.form.get('dict') == "Camel":
            dict = "camelo"
    return render_template('draw.html', user=current_user, dict=dict)


@views.route('/grading', methods=['POST'])
def grading():
    global graph
    with graph.as_default():
        if request.method == 'POST':
            final_pred = None
            draw = request.form['url']
            draw = draw[init_Base64:]
            draw_decoded = base64.b64decode(draw)
            image = np.asarray(bytearray(draw_decoded), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_UNCHANGED)
            # img = Image.fromarray(image)
            # img.show()

    return render_template('grading.html', grading='Hi there', user=current_user)


@views.route('/save', methods=['POST'])
def save():

    if request.method == 'POST':
        if request.form.get('dict') == "gato":
            message = "O gato foi salvo!"
        elif request.form.get('dict') == "girafa":
            message = "A girafa foi salva!"
        elif request.form.get('dict') == "ovelha":
            message = "A ovelha foi salva!"
        elif request.form.get('dict') == "morcego":
            message = "O morcego foi salvo!"
        elif request.form.get('dict') == "polvo":
            message = "O polvo foi salvo!"
        elif request.form.get('dict') == "camelo":
            message = "O camelo foi salvo!"
    return render_template('save.html', user=current_user, message=message)

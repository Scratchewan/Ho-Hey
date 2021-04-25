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
from PIL import Image
import pandas as pd

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
            height = image.shape[0]
            width = image.shape[1]
            background = np.zeros([width, width, 3], dtype=np.uint8)
            background.fill(0)
            background = Image.fromarray(background)
            background.paste(Image.fromarray(image),
                             (0, (int((width-height)/2))))
            pil_image = background.convert('RGB')
            open_cv_image = np.array(pil_image)
            open_cv_image = open_cv_image[:, :, 0].copy()
            resized = cv2.resize(open_cv_image, (28, 28),
                                 interpolation=cv2.INTER_AREA)
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
            image = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)
            height = image.shape[0]
            width = image.shape[1]
            background = np.zeros([width, width, 3], dtype=np.uint8)
            background.fill(0)
            background = Image.fromarray(background)
            background.paste(Image.fromarray(image),
                             (0, (int((width-height)/2))))
            pil_image = background.convert('RGB')
            open_cv_image = np.array(pil_image)
            open_cv_image = open_cv_image[:, :, 0].copy()
            resized = cv2.resize(open_cv_image, (28, 28),
                                 interpolation=cv2.INTER_AREA)
            vect = np.asarray(resized, dtype="uint8")
            vect = vect.reshape(1, 1, 28, 28).astype('float32')
            my_prediction = model.predict(vect)
            df = pd.DataFrame(my_prediction)
            dict = request.form.get('dict')
            if dict == "gato":
                index = 0
                pronoun = 'Seu'
            elif dict == "girafa":
                index = 1
                pronoun = 'Sua'
            elif dict == "ovelha":
                index = 2
                pronoun = 'Sua'
            elif dict == "morcego":
                index = 3
                pronoun = 'Seu'
            elif dict == "polvo":
                index = 4
                pronoun = 'Seu'
            elif dict == "camelo":
                index = 5
                pronoun = 'Seu'
            value = df[index].values[0]
            grading = int(value * 10)
            message = pronoun + ' ' + dict + \
                ' ficou  nota ' + str(grading) + '!'
    return render_template('grading.html', dict=dict, message=message, user=current_user)


@views.route('/save', methods=['POST'])
def save():
    global graph
    with graph.as_default():
        if request.method == 'POST':
            final_pred = None
            draw = request.form['url']
            draw = draw[init_Base64:]
            draw_decoded = base64.b64decode(draw)
            image = np.asarray(bytearray(draw_decoded), dtype="uint8")
            # image = cv2.imdecode(image, cv2.IMREAD_UNCHANGED)
            # img = Image.fromarray(image)
            # img.show()

        dict = request.form.get('dict')
        global message
        message = ""
        if dict == "gato":
            message = "O gato foi salvo!"
        elif dict == "girafa":
            message = "A girafa foi salva!"
        elif dict == "ovelha":
            message = "A ovelha foi salva!"
        elif dict == "morcego":
            message = "O morcego foi salvo!"
        elif dict == "polvo":
            message = "O polvo foi salvo!"
        elif dict == "camelo":
            message = "O camelo foi salvo!"
        elif dict == "desenho":
            message = "O desenho foi salvo!"
    return render_template('save.html', dict=dict, message=message, user=current_user)

import os

from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import logging, traceback

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
log_handler = logging.FileHandler(os.getenv('LOG_FILE'))
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(name)s - %(funcName)s - %(message)s')
log_handler.setFormatter(formatter)
log_handler.setLevel(logging.DEBUG)
app.logger.addHandler(log_handler)
log = app.logger

flag = os.getenv('DEBUG')
if flag == '0':
    from mysql_model import Person, Human
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
else:
    from test_model import Person, Human
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI2')

app.config['PORT'] = os.getenv('PORT')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/')
def index():
    return 'Response Data'

@app.route('/another')
def another():
    return 'Another Response'

@app.route('/test_request')
def test_request():
    return f'test_request:{request.args.get("dummy")}'

@app.route('/exercise_request/<box>')
def exercise_request(box):
    return f'Hello, {box} .'

@app.route('/show_html')
def show_html():
    return render_template('test_html.html')

@app.route('/exercise_html')
def exercise_html():
    return render_template('exercise.html')

@app.route('/exercise')
def excersize():
    return f'{request.args.get("my_name")}さん、ようこそ'

@app.route('/try_rest', methods=["POST"])
def try_rest():
    request_json = request.get_json()
    print(request_json)
    #print(type(request_json))
    
    #name = request_json['name']
    #print(name)

    for a in request_json['friends']:
        print(a)

    response_json = {"response_json" : request_json}
    return jsonify(response_json)

@app.route('/person_search')
def person_search():
    return render_template('./person_search.html')

@app.route('/person_result')
def person_result():
    try:
        search_size = request.args.get("search_size")
        log.debug(f'search_size:{search_size}')
        search_size = int(search_size)
        persons = db.session.query(Person).filter(Person.size > search_size)
    except Exception:
        log.error(traceback.format_exec())
    return render_template('./person_result.html', persons=persons, search_size=search_size)

@app.route('/human_search')
def human_search():
    return render_template('./human_search.html')

@app.route('/human_result')
def human_result():
    try:
        height = request.args.get("height")
        weight = request.args.get("weight")
        log.debug(f'height:{height} weight:{weight}')
        height = int(height)
        weight = int(weight)
        humans = db.session.query(Human).filter(Human.height >= height, Human.weight >= weight)
    except Exception:
        log.error(traceback.format_exc())
    return render_template("./human_result.html", humans=humans, height=height, weight=weight)

@app.route('/try_html')
def try_html():
    return render_template("./try_html.html")

@app.route('/show_data', methods=["GET","POST"])
def show_data():
    return f'{request.form.get("text_input")}'

from flask import Flask, render_template, request 
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import sqlite3 as sql
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

## TODO Database Setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

CORS(app)

## MODEL
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Boolean)

    def __repr__(self):
        return f'Task: {self.description}'
    
    def __init__(self, description):
        self.description = description
        self.status = False


def format_task(task):
    return {
        'id' : task.id,
        'description' : task.description,
        'status' : task.status
    }


## TODO ROUTES
## TODO GET ALL TASKS
@app.route('/tasks', methods=['GET'])
def get_posts():
    tasks = Task.query.order_by(Task.id.asc()).all()
    task_list = [(format_task(task)) for task in tasks]
    
    return {
        'tasks' : task_list
    }

## TODO GET ONE TASK
@app.route('/task/<id>', methods=['GET'])
def get_post(id):
    task = Task.query.filter_by(id=id).one()
    fmt_task = format_task(task)

    return fmt_task

## TODO CREATE TASK
@app.route('/task', methods=['POST'])
def create_task():
    description = request.json['description']

    new_task = Task(description)
    db.session.add(new_task)
    db.session.commit()
    
    return format_task(new_task)

## TODO UPDATE TASK
@app.route('/task/<id>', methods=['PATCH'])
def update_task(id):
    task = Task.query.filter_by(id=id)
    if 'description' in request.json:
        description = request.json['description']
        task.update(dict(description = description))
    if 'status' in request.json:
        status = request.json['status']
        task.update(dict(status=status))

    db.session.commit()

    return {
        'task' : format_task(task.one())
    }

## TODO DELETE TASK
@app.route('/task/<id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.filter_by(id=id).one()
    db.session.delete(task)
    db.session.commit()
    
    return f'Task {id} has been deleted.'

## MAIN
if __name__ == '__main__':
    app.run(debug=True)
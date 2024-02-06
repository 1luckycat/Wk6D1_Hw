from flask import Blueprint, render_template

dog = Blueprint('dog', __name__, template_folder = 'dog_templates')

@dog.route('/')
def dogs():
    return render_template('dog.html')
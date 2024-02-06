from flask import Blueprint, render_template

bird = Blueprint('bird', __name__, template_folder = 'bird_templates')

@bird.route('/')
def birds():
    return render_template('bird.html')
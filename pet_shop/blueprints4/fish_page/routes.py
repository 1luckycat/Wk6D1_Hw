from flask import Blueprint, render_template

fish = Blueprint('fish', __name__, template_folder = 'fish_templates')

@fish.route('/')
def fishes():
    return render_template('fish.html')
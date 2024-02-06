from flask import Blueprint, render_template

reptile = Blueprint('reptile', __name__, template_folder = 'reptile_templates')

@reptile.route('/')
def reptiles():
    return render_template('reptile.html')
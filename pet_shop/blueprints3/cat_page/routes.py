from flask import Blueprint, render_template

cat = Blueprint('cat', __name__, template_folder = 'cat_templates')

@cat.route('/')
def cats():
    return render_template('cat.html')
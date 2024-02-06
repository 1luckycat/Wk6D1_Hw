from flask import Flask
from config import Config
from .blueprints.site.routes import site
from .blueprints2.dog_page.routes import dog
from .blueprints3.cat_page.routes import cat
from .blueprints4.fish_page.routes import fish
from .blueprints5.bird_page.routes import bird
from .blueprints6.reptile_page.routes import reptile

app = Flask(__name__)

app.config.from_object(Config)

app.register_blueprint(site)
app.register_blueprint(dog, url_prefix='/dogs')
app.register_blueprint(cat, url_prefix='/cats')
app.register_blueprint(fish, url_prefix='/fishes')
app.register_blueprint(bird, url_prefix='/birds')
app.register_blueprint(reptile, url_prefix='/reptiles')

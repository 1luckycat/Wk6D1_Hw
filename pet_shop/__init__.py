from flask import Flask
from flask_migrate import Migrate


# internal imports
from config import Config
from .blueprints.site.routes import site
from .blueprints2.dog_page.routes import dog
from .blueprints3.cat_page.routes import cat
from .blueprints4.fish_page.routes import fish
from .blueprints5.bird_page.routes import bird
from .blueprints6.reptile_page.routes import reptile
from .models import login_manager, db
from .blueprints.auth.routes import auth


app = Flask(__name__)

app.config.from_object(Config)


login_manager.init_app(app)
login_manager.login_view = 'auth.sign_in'
login_manager.login_message = "Please log in!"
login_manager.login_message_category = 'warning'


app.register_blueprint(site)
app.register_blueprint(dog, url_prefix='/dogs')
app.register_blueprint(cat, url_prefix='/cats')
app.register_blueprint(fish, url_prefix='/fishes')
app.register_blueprint(bird, url_prefix='/birds')
app.register_blueprint(reptile, url_prefix='/reptiles')
app.register_blueprint(auth)


db.init_app(app)
migrate = Migrate(app, db)
import connexion

from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo
import dns

app = connexion.App(__name__, specification_dir='./openapi_server/openapi/')
app.app.config.from_pyfile("./config.py")
print(app.app.config)
## https://stackoverrun.com/ja/q/11355897
# must need packagename
app.app.config.from_object('openapi_server.config.DevelopmentConfig')
app.app.config["MONGO_URI"] = "mongodb+srv://" + app.app.config['BSVCONTENTSERVER_MONGODB_USER'] + ":" + app.app.config['BSVCONTENTSERVER_MONGODB_PASS'] + "@cluster0-xhjo9.mongodb.net/test?retryWrites=true&w=majority"

bootstrap = Bootstrap(app.app)
mongo = PyMongo(app.app)


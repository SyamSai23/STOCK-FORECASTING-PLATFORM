from flask import Flask
from routes.allRoutes import bp_route
from flask_cors import CORS
# other imports as necessary

app = Flask(__name__)
CORS(app)

# Register blueprints

app.register_blueprint(bp_route)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
   #app.run(host='0.0.0.0', port=9600, debug=True)

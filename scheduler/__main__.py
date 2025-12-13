from flask import Flask
import predictionsBLUEPRINT
from flask_cors import CORS
# other imports as necessary

app = Flask(__name__)
CORS(app)

# Register blueprints

app.register(predictionsBLUEPRINT)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9600, debug=True)

# All imports
from flask import Flask, render_template, request, jsonify


### Backend implementation must go here ######################

def checkGrammar(data):
    # Dummy grammar correction for now
    return data.upper()

###############################################################


# Open flask
app = Flask(__name__)

# Serve the main file. We have stored this in templates directory
@app.route('/')
def index():
    return render_template('index.html')

# This is to handle the process data function that will be called form our javascript
@app.route('/process_data', methods=['POST'])
def process_data():
    # Collect data
    data = request.get_json()
    # Process data: check the grammar and give reply
    result = {"message": f"Corrected: {checkGrammar(data['value'])}"}
    # Send it back
    return jsonify(result) 

# If run on its own as main app
if __name__ == '__main__':
    app.run(debug=True)
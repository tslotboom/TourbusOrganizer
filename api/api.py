from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/getExcelFile', methods = ['POST'])
def getExcelFile():
    data = request.json.get('data')
    print(data)
    return {"Data": f"Received data {data}"}


if __name__== "__main__": 
    app.run(debug=True)
from flask import Flask, request
from flask_cors import CORS
from ..src.MakeExcelFile import makeExcelFile


app = Flask(__name__)
CORS(app)

@app.route('/getExcelFile', methods = ['POST'])
def getExcelFile():
    data = request.json
    numDays = request.json.get('numDays')
    tourists = request.json.get('tourists')
    print(numDays, tourists)
    makeExcelFile(data)
    return {"Data": f"Received data "}


if __name__== "__main__": 
    app.run(debug=True)

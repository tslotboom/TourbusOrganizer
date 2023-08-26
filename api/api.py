from flask import Flask, request


app = Flask(__name__)


@app.route('/getExcelFile', methods = ['POST'])
def getExcelFile():
    data = request.json.get('data')
    print(data)
    return f"Received data {data}"
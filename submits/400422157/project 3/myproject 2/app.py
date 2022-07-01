from flask import Flask, request, jsonify, render_template, send_file
from utils.common import read_json_time_series
from utils.methods import linear_interpolation, interpolation_service1, interpolation_service2, sampling, outlierDetection
import json

app = Flask(__name__)


@app.route('/')
def isup():
    return render_template("index.html")

@app.route('/homepage', methods=['POST'])
def homepage():
    return render_template("index.html")

@app.route('/service1', methods=['POST'])
def service1():
    file = request.files["file"]
    filejson = json.load(file)
    #req = request.get_json()
    data = filejson['data']
    file_data = open("data.json", 'w')
    data = str(data)
    data = data.replace("\'", "\"")
    file_data.write(data)
    file_data.close()
    f = open("data.json", 'r')
    ff = f.read()
    f.close()
    config = filejson["config"]
    data = read_json_time_series(ff)
    data_new = interpolation_service1(data, config["type"],config["time"], config["interpolation"])
    if(isinstance(data_new, str)):
        return render_template("result.html", title = "result of service1", result=data_new)
    print(data_new["time"])
    print(data_new.to_json(orient='columns'))
    f = open("json_data.json", "w")
    f.write(data_new.to_json(orient='columns'))
    f.close()
    with open('json_data.json', 'r') as json_file:
        json_object = json.load(json_file)
    print(json_object)
    print(json.dumps(json_object))
    print(json.dumps(json_object, indent=1))
    result = json.dumps(json_object, indent=1)
    with open("output.json", "w") as outfile:
        outfile.write(json.dumps(json_object, indent=1))
    with open("output.json", "r") as outfile:
        #result = json.load(outfile)    
        result = outfile.read()
    print(result)    
    result = result.replace('\n', '<br>')
    print(result)
    return render_template("result.html", title = "result of service1", result=result)


@app.route('/service2', methods=['GET', 'POST'])
def service2():
    file = request.files["file"]
    filejson = json.load(file)
    #req = request.get_json()
    data = filejson['data']
    file_data = open("data.json", 'w')
    data = str(data)
    data = data.replace("\'", "\"")
    file_data.write(data)
    file_data.close()
    f = open("data.json", 'r')
    ff = f.read()
    f.close()
    #datajson = json.load(f)
    config = filejson["config"]
    data = read_json_time_series(ff)
    data_new = interpolation_service2(data,config["time"], config["interpolation"])
    if(isinstance(data_new, str)):
        return render_template("result.html", title = "result of service2", result=data_new)
    print(data_new["time"])
    print(data_new.to_json(orient='columns'))
    f = open("json_data.json", "w")
    f.write(data_new.to_json(orient='columns'))
    f.close()
    with open('json_data.json', 'r') as json_file:
        json_object = json.load(json_file)
    print(json_object)
    print(json.dumps(json_object))
    print(json.dumps(json_object, indent=1))
    result = json.dumps(json_object, indent=1)
    with open("output.json", "w") as outfile:
        outfile.write(json.dumps(json_object, indent=1))
    with open("output.json", "r") as outfile:
        #result = json.load(outfile)    
        result = outfile.read()
    print(result)    
    result = result.replace('\n', '<br>')
    print(result)   
    return render_template("result.html", title = "result of service2",result=result)

@app.route('/service3', methods=['GET', 'POST'])
def service3():
    file = request.files["file"]
    filejson = json.load(file)
    #req = request.get_json()
    data = filejson['data']
    file_data = open("data.json", 'w')
    data = str(data)
    data = data.replace("\'", "\"")
    file_data.write(data)
    file_data.close()
    f = open("data.json", 'r')
    ff = f.read()
    f.close()
    #datajson = json.load(f)
    config = filejson["config"]
    data = read_json_time_series(ff)
    print((config["time_series"]))
    data_new = outlierDetection(data, config["time_series"])
    #print(new_data) 
    #print(data_new["time"])
    print(data_new.to_json(orient='columns'))
    f = open("json_data.json", "w")
    f.write(data_new.to_json(orient='columns'))
    f.close()
    with open('json_data.json', 'r') as json_file:
        json_object = json.load(json_file)
    print(json_object)
    print(json.dumps(json_object))
    print(json.dumps(json_object, indent=1))
    result = json.dumps(json_object, indent=1)
    with open("output.json", "w") as outfile:
        outfile.write(json.dumps(json_object, indent=1))
    with open("output.json", "r") as outfile:
        #result = json.load(outfile)    
        result = outfile.read()
    print(result)    
    result = result.replace('\n', '<br>')
    print(result)
    return render_template("result.html", title = "result of service3",result=result)  


@app.route('/service4', methods=['GET', 'POST'])
def service4():
    file = request.files["file"]
    filejson = json.load(file)
    #req = request.get_json()
    data = filejson['data']
    file_data = open("data.json", 'w')
    data = str(data)
    data = data.replace("\'", "\"")
    file_data.write(data)
    file_data.close()
    f = open("data.json", 'r')
    ff = f.read()
    f.close()
    #datajson = json.load(f)
    config = filejson["config"]
    data = read_json_time_series(ff)
    data_new = sampling(data, config["method"])
    print(data_new)
    #print(data_new["time"])
    print(data_new.to_json(orient='columns'))
    f = open("json_data.json", "w")
    f.write(data_new.to_json(orient='columns'))
    f.close()
    with open('json_data.json', 'r') as json_file:
        json_object = json.load(json_file)
    print(json_object)
    print(json.dumps(json_object))
    print(json.dumps(json_object, indent=1))
    result = json.dumps(json_object, indent=1)
    with open("output.json", "w") as outfile:
        outfile.write(json.dumps(json_object, indent=1))
    with open("output.json", "r") as outfile:
        #result = json.load(outfile)    
        result = outfile.read()
    print(result)    
    result = result.replace('\n', '<br>')
    print(result)
    return render_template("result.html", title = "result of service4",result=result) 

@app.route('/download', methods=['GET', 'POST'])
def downloadFile ():
    path = "output.json"
    return send_file(path, as_attachment=True)   

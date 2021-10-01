from flask import Flask,render_template,request,jsonify,url_for
import pickle
import numpy as np
from requests import post
import json

#load the venues
with open('venue.json','r') as f:
    venues = json.load(f)    
#Load the model 
filename = 'first-innings-score-lasso-model.pkl'
regressor = pickle.load(open(filename,'rb'))

app = Flask(__name__)



@app.route('/')
def home():
    return render_template('index.html',venue  = venues)


@app.route('/example/<lower_limit>/<upper_limit>')
def example(lower_limit,upper_limit):
    return render_template("result.html", lower_limit=lower_limit,upper_limit=upper_limit)


@app.route('/predict',methods=['POST'])

def predict():
    temp_arr = list()

    
    batting_team = request.json['batting']
    if batting_team=='Chennai Super Kings':
        temp_arr += [1,0,0,0,0,0,0,0]
    elif batting_team == 'Delhi Daredevils':
        temp_arr = temp_arr + [0,1,0,0,0,0,0,0]
    elif batting_team == 'Kings XI Punjab':
        temp_arr = temp_arr + [0,0,1,0,0,0,0,0]
    elif batting_team == 'Kolkata Knight Riders':
        temp_arr = temp_arr + [0,0,0,1,0,0,0,0]
    elif batting_team == 'Mumbai Indians':
        temp_arr = temp_arr + [0,0,0,0,1,0,0,0]
    elif batting_team == 'Rajasthan Royals':
        temp_arr = temp_arr + [0,0,0,0,0,1,0,0]
    elif batting_team == 'Royal Challengers Bangalore':
        temp_arr = temp_arr + [0,0,0,0,0,0,1,0]
    elif batting_team == 'Sunrisers Hyderabad':
        temp_arr = temp_arr + [0,0,0,0,0,0,0,1]



    bowling_team = request.json['bowling']
    if bowling_team == 'Chennai Super Kings':
        temp_arr = temp_arr + [1,0,0,0,0,0,0,0]
    elif bowling_team == 'Delhi Daredevils':
        temp_arr = temp_arr + [0,1,0,0,0,0,0,0]
    elif bowling_team == 'Kings XI Punjab':
        temp_arr = temp_arr + [0,0,1,0,0,0,0,0]
    elif bowling_team == 'Kolkata Knight Riders':
        temp_arr = temp_arr + [0,0,0,1,0,0,0,0]
    elif bowling_team == 'Mumbai Indians':
        temp_arr = temp_arr + [0,0,0,0,1,0,0,0]
    elif bowling_team == 'Rajasthan Royals':
        temp_arr = temp_arr + [0,0,0,0,0,1,0,0]
    elif bowling_team == 'Royal Challengers Bangalore':
        temp_arr = temp_arr + [0,0,0,0,0,0,1,0]
    elif bowling_team == 'Sunrisers Hyderabad':
        temp_arr = temp_arr + [0,0,0,0,0,0,0,1]
    
    venue = request.json["venues"]
    
    temp_ven = [0]*10
    for i in venues:
        if i =='venue':
            ind = venues[i]
            temp_ven.insert(ind,1)
            break


    

        


    overs = float(request.json['over'])
    runs = int(request.json['run'])
    wickets = int(request.json['wicket'])
    runs_in_prev_5 = int(request.json['run_last5'])
    wickets_in_prev_5 = int(request.json['wicket_last5']) 


    temp_arr = temp_arr + temp_ven+ [overs,runs,wickets,runs_in_prev_5,wickets_in_prev_5]
    

    data = np.array([temp_arr][0])
    data = data.reshape(1,31)
    my_prediction = int(regressor.predict(data)[0])
    
    

    return jsonify({'redirect': url_for("example", lower_limit=my_prediction-10,upper_limit = my_prediction+5)})

        


if __name__ == '__main__':
    app.run(debug=True,port=8000)

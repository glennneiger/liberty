from flask import Flask, request, jsonify, render_template
import os
import dialogflow
import requests
import json
import pusher

global maincat
maincat=""
global success
success=False # default is false
app = Flask(__name__)

# initialize Pusher
pusher_client = pusher.Pusher(
  app_id='701796',
  key='92992f27c9efddd649df',
  secret='c23ec3c8895c227e0128',
  cluster='us2',
  ssl=True
)
# Employee Database holder
employee_db = {'12345': ['robert', 'robert@2019', 'Robert'], '12346': ['arthur', 'arthur@2019', 'Arthur'], '12347': ['cobb', 'cobb@2019', 'Cobb'],
               '12348': ['bruce', 'bruce@2019', 'Bruce'], '12349': ['ariadne', 'ariadne@2019', 'Ariadne']}

# Main Category to Sub Categories holder
categories = {'Disciplinary': ['Drugs and Violence', 'Other Disciplinary Actions'], 'Behavior': ['Outside of Work', 'Business Conduct', 'Professionality'],
            'Benefits': ['Medical Benefits', 'Other Benefits'], 'General': ['Introduction to Company', 'Hours', 'Company Guidelines', 'Work'],
            'Salary': ['Refunds and Deductions', 'Pay']}

def buttons(categories, success, maincat):
    if(success==True):
        if(maincat == ''):
            return list(categories.keys())
        else:
            return categories[maincat]
    else:
        return None;


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/get_login_detail', methods=['POST'])
def get_login_detail():
    global maincat
    global success
    data = request.get_json(silent=True)
    response = ""
    try:
        if data['queryResult']['action'] == 'employee_username':
            print('Check 1')
            response = "Username and Password do not match, what is your username?"
            userid = data['queryResult']['parameters']['user_id']
            password = data['queryResult']['parameters']['password']
            print("Username data type: ", type(userid))
            print("Password data type: ", type(password))
            print('User ID: ', userid, 'Password: ', password)
            print("Expected Password: ", employee_db[userid][1])
            if(userid in employee_db.keys()):
                if(employee_db[userid][1]==password):
                    success=True
                    print(success)
                    response = "Welcome {0}, what category would you like to find out more about today?".format(employee_db[userid][2])
        if data['queryResult']['action'] == 'MainCat':
            print('check 2')
            response = "Category doesn't exist, choose another one"
            maincat = data['queryResult']['parameters']['maincat']
            if(maincat in categories.keys()):
                subs = ''
                for i in range(0, len(categories[maincat])-1):
                    subs += categories[maincat][i] + ', '
                subs += 'or '+categories[maincat][len(categories[maincat])-1]
                response = 'Under {0}, would you like to find out more about {1}?'.format(maincat, subs)

    except:
        response = ""

    reply = {
        "fulfillmentText": response
    }

    return jsonify(reply)


def detect_intent_texts(project_id, session_id, text, language_code):
    print("Check")
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    if text:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)
        return response.query_result.fulfillment_text


@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    print(message)
    project_id = 'liberty-735ff'
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')
    print("Success Status: ", success)
    response_text = {"message": fulfillment_text, "key":success, "buttons": buttons(categories, success, maincat)}
    socketId = request.form['socketId']
    pusher_client.trigger('liberty', 'new_message',
                          {'human_message': message, 'bot_message': fulfillment_text}, socketId)
    print(fulfillment_text)
    print(response_text)
    return jsonify(response_text)


# run Flask app
if __name__ == "__main__":
    app.run()
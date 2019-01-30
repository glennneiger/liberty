from flask import Flask, request, jsonify, render_template
# import os
import dialogflow
# import requests
import json
import pusher

global maincat

maincat=''

global success

success=False

global subcat

subcat=''


# default is false
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


j = json.loads(open('categories.json').read())


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/get_login_detail', methods=['POST'])
def get_login_detail():
    data = request.get_json(silent=True)
    response = ""
    global maincat
    global success
    global subcat
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
                    print("Yes")
                    success=True
                    response = "Welcome {0}, what category would you like to find out more about today?".format(employee_db[userid][2])
        if data['queryResult']['action'] == 'MainCat':
            print('check 2')
            response = "Category doesn't exist, choose another one"
            maincat = data['queryResult']['parameters']['maincat']
            if(maincat in j.keys()):
                subs = ''
                subcats = list(j[maincat].keys())
                print(subcats)
                for i in range(0, len(subcats)-1):
                    print(i)
                    subs += subcats[i] + ', '
                    print(subs)
                subs += 'or '+subcats[len(subcats)-1]
                response = 'Under {0}, would you like to find out more about {1}?'.format(maincat, subs)
        if data['queryResult']['action'] == 'subcategory':
            print('check 3')
            response = "Sub Category doesn't exist, choose another one"
            subcat = data['queryResult']['parameters']['subcat']
            print("Subcat: ", subcat)
            print(type(subcat))
            print("Maincat: ", cat)
            print(j[cat].keys())
            if(subcat in j[cat].keys()):
                print('Entered Key Value')
                leafs = j[cat][subcat]
                print('Category: ', cat)
                print('Leafs: ', leafs)
                choices = ''
                for i in range(0, len(leafs)-1):
                    print(i)
                    choices += leafs[i] + ', '
                    print(choices)

                choices += 'or ' + leafs[-1]
                response = 'Under {0}, would you like to find out more about {1}?'.format(subcat, choices)

    except:
        response = ""

    reply = {
        "fulfillmentText": response
    }

    return jsonify(reply)

def buttons(j, success, maincat, subcat):
    if(success==True):
        if(maincat == ''):
            return list(j.keys())
        else:
            if(subcat == ''):
                return list(j[maincat].keys())
            else:
                return j[maincat][subcat]
    else:
        return None;



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
    b = buttons(j, success, maincat, subcat)
    response_text = {"message": fulfillment_text, "key":success, "buttons": b}
    print('Button value: ', b)
    print("Main Category: ", maincat)
    print("Sub Category: ", subcat)
    socketId = request.form['socketId']
    pusher_client.trigger('liberty', 'new_message',
                          {'human_message': message, 'bot_message': fulfillment_text}, socketId)
    print(fulfillment_text)
    print(response_text)
    return jsonify(response_text)


# run Flask app
if __name__ == "__main__":
    app.run()
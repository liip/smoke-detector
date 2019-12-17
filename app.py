# coding=utf-8
from flask import Flask, request, render_template
import requests, json, os

app = Flask(__name__)

# ENVIRONMENT VARIABLE
APP_URL = os.environ['APP_URL']
SLACK_URL = os.environ['SLACK_URL']
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']

# GLOBAL VARIABLE
SCOPE = 'read_smokedetector'

@app.route('/', methods=['GET', 'POST'])
def home():

    request_url = 'https://api.netatmo.com/oauth2/authorize?client_id=' + CLIENT_ID + '&redirect_uri=' + APP_URL + '/netatmoOAuth&scope=' + SCOPE + '&state=abcd'
    return render_template('index.html', url = request_url)

@app.route('/netatmoOAuth', methods=['GET'])
def netatmoOAuth():

    # GET USER CODE
    code_user = request.args.get('code')

    # CALL NETATMO TO RETRIEVE TOKEN
    host_url = 'https://api.netatmo.com/oauth2/token'
    request_datas = {
        'grant_type' : 'authorization_code',
        'client_id' : CLIENT_ID,
        'client_secret' : CLIENT_SECRET,
        'code' : code_user,
        'redirect_uri' : APP_URL + '/netatmoOAuth',
        'scope' : SCOPE
    }

    # GET ACCESS TOKEN
    json_return = requests.post(host_url, data = request_datas)
    access_token = json_return.json()['access_token']

    # ADD WEB HOOK
    add_web_hook_url = 'https://api.netatmo.com/api/addwebhook?url=' + APP_URL + '/webhook'
    json_return = requests.get(add_web_hook_url, headers = {'Authorization' : 'Bearer ' + access_token})
    web_hook_status = json_return.json()['status']

    # VERIFY WEB HOOK
    if web_hook_status == "ok":
        return render_template('success.html')

    return render_template('error.html')

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():

    # VERIFY JSON
    json_file = request.json
    if json_file == None:
        slackMessage("JSON is null.")
        return "JSON is null."

    # SHOW JSON IN LOG
    app.logger.info('request json : %s', request.json)

    # GET JSON
    json_event_type = json_file['event_type']
    event_type = json.dumps(json_event_type).strip('"')
    sub_type = json_file['sub_type']

    # HUSHED
    if event_type == "hush":
        slackMessage("Alarm hushed for 15 min !")
        return "Alarm hushed for 15 min !"

    # WIFI
    if event_type == "wifi_status":
        if sub_type == 0:
            slackMessage("Wifi Error !")
            return "Wifi Error !"
        if sub_type == 1:
            slackMessage("Wifi Ok !")
            return "Wifi Ok !"

    # SOUND TEST
    if event_type == "sound_test":
        if sub_type == 0:
            slackMessage("Sound Test Ok !")
            return "Sound Test Ok !"
        if sub_type == 1:
            slackMessage("Sound Test Error !")
            return "Sound Test Error !"

    # SMOKE
    if event_type == "smoke":
        if sub_type == 0:
            slackMessage("Smoke is cleared !")
            return "Smoke is cleared !"
        if sub_type == 1:
            slackMessage("Smoke is detected !")
            return "Smoke is detected !"

    # BATTERY
    if event_type == "battery_status":
        if sub_type == 0:
            slackMessage("Battery is low !")
            return "Battery is low !"
        if sub_type == 1:
            slackMessage("Battery is very low !")
            return "Battery is very low !"

    # OTHER EVENT
    slackMessage("Unknown event: " + event_type)

    return "Unknown event: " + event_type

def slackMessage(text):

    slack_msg = {"text" : text}
    requests.post(SLACK_URL, data=json.dumps(slack_msg))
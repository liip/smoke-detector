# 🚭 Smoke-Detector
Allow us to be notified when there is smoke in the office.  
Blog post :  https://www.liip.ch/blog/smoke-detector-for-device-lab  
Netatmo API : https://dev.netatmo.com/
## Clone repository
```shell
$ git clone https://github.com/liip/smoke-detector.git
```


## Development

### Virtualenv
```shell
# Install virtualenv
$ pip install virtualenv

# Use python3 in virtualenv
$ virtualenv -p python3 env

# Active virtual env
$ source env/bin/activate
```

### Install dependencies
```shell
$ pip install -r requirements.txt
```

### Initialize environment variables
```shell
# Define URL of app
$ export APP_URL='https://yourAppURL'

# Define Slack WebHook URL
$ export SLACK_URL='https://yourWebHookURL'

# Define client ID key
$ export CLIENT_ID='yourClientIDKey'

# Define client secret key
$ export CLIENT_SECRET='yourClientSecretKey'
```


### Start server
```shell
# Active auto-reloading
$ export FLASK_ENV=development

# Define app
$ export FLASK_APP=app.py

# Start server
$ flask run
```
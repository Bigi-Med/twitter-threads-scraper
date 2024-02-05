# importing libraries 
from flask import Flask, request
from flask_mail import Mail, Message 
import subprocess
import logging
import os
import json
from flask_cors import CORS  # Import CORS from flask_cors

app = Flask(__name__) 
CORS(app)

@app.route("/")
def index():
    profile = request.args.get('profile')
    print(profile)
    return 'sent'

if __name__ == '__main__': 
    app.run(host='0.0.0.0') 
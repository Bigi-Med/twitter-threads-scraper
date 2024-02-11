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
scrapy_project_path = os.path.join(os.path.dirname(__file__),'scraper','twitterthreads')
output_file_path = os.path.join(scrapy_project_path,'profile.json')

@app.route("/")
def index():
    profile = request.args.get('profile')
    print("Executing spider .....")
    # subprocess.run(['scrapy','crawl','ThreadsScraper','-o',output_file_path,'-a','profile='+profile],cwd = scrapy_project_path)
    subprocess.run(['scrapy','crawl','ThreadsScraper','-a','profile='+profile],cwd = scrapy_project_path)

    with open(output_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    
    print(data)
    
    return data

if __name__ == '__main__': 
    app.run(host='0.0.0.0') 

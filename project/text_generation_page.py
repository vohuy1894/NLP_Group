import os

import random
from flask import request
from flask import Flask, render_template
from transformers import pipeline

output_text = "Output will display here"

alice_model = pipeline('text-generation', model="models/Alice_fine_tuned", tokenizer='xlnet-base-cased')
genesis_model = pipeline('text-generation', model="models/Genesis_KJV_fine_tuned", tokenizer='gpt2')
sherlock_model = pipeline('text-generation', model="models/Sherlock_Holmes_fine_tuned", tokenizer='gpt2')

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('Text Generation Page.html', output_text=output_text)
    
@app.route('/adjust_text', methods=["POST"])
def adjust_text():
    model = request.form['b']
    if model == "Alice In Wonderland":
        print('Alice')
        output_text = alice_model(request.form['a'])[0]['generated_text']
    elif model == "Sherlock Holmes":
        print('Sherlock')
        output_text = genesis_model(request.form['a'])[0]['generated_text']
    elif model == "Genesis":
        print('Genesis')
        output_text = sherlock_model(request.form['a'])[0]['generated_text']
    print(output_text)
    return render_template('Text Generation Page.html', output_text=output_text)
    

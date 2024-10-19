from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS
import openai
from openai import OpenAI

import os
import traceback  # For detailed error logging

app = Flask(__name__)
# CORS(app)

# Enable CORS for all routes; adjust origins for security as needed
client = OpenAI(api_key="")

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

# User authentication and health-related routes (your friend's code)
@app.route('/')
def start():
    return render_template('symptomchecker.html')

@app.route('/suggestion', methods=['GET'])
def suggestion():
    suggestions = "Here are your diet and lifestyle suggestions based on your data."
    return render_template('suggestion.html', suggestions=suggestions)

@app.route('/epharmacy', methods=['GET'])
def epharmacy():
    return render_template('epharmacy.html')

# Chatbox feature (your code)
@app.route('/chat-mental', methods=['POST'])
def chat_mental():
    try:
        user_message = request.json.get('message', '')

        if not user_message:
            return jsonify({'reply': 'Please enter a valid message.'}), 400

        # Call to OpenAI's ChatGPT API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful mental health AI assistant."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150
        )

        ai_reply = response.choices[0].message.content 
        return jsonify({'reply': ai_reply})

    except openai.error.OpenAIError as e:
        error_message = f"OpenAI API error: {e}"
        print(error_message)
        return jsonify({'reply': 'Error from OpenAI API.'}), 500

    except Exception as e:
        error_message = f"Unexpected error: {e}\n{traceback.format_exc()}"
        print(error_message)
        return jsonify({'reply': 'Sorry, something went wrong.'}), 500

@app.route('/chat-physical', methods=['POST'])
def chat_physical():
    # try:
        user_message = request.json.get('message', '')

        if not user_message:
            return jsonify({'reply': 'Please enter a valid message.'}), 400

        # Call to OpenAI's ChatGPT API for physical health
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful physical health AI assistant."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150
        )

        ai_reply = response.choices[0].message.content
        return jsonify({'reply': ai_reply})

    # except openai.error.OpenAIError as e:
    #     error_message = f"OpenAI API error: {e}"
    #     print(error_message)
    #     return jsonify({'reply': 'Error from OpenAI API.'}), 500

    # except Exception as e:
    #     error_message = f"Unexpected error: {e}\n{traceback.format_exc()}"
    #     print(error_message)
    #     return jsonify({'reply': 'Sorry, something went wrong.'}), 500

if __name__ == '__main__':
    app.run(debug=True)

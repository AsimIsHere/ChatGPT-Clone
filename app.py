from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from config import api
import logging
from waitress import serve

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Configure the Gemini API
genai.configure(api_key=api)  # Replace with your actual API key

def chat(query):
    model = genai.GenerativeModel('gemini-pro')  # For text generation
    try:
        response = model.generate_content(query)
        return response.text
    except Exception as e:
        app.logger.error(f"Error generating content: {e}")
        return "Error generating response."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    try:
        data = request.get_json()
        query = data.get('query')
        app.logger.debug(f'Received query: {query}')
        response_text = chat(query)
        app.logger.debug(f'Response: {response_text}')
        return jsonify({'response': response_text})
    except Exception as e:
        app.logger.error(f"Error processing request: {e}")
        return jsonify({'response': 'Error processing request.'}), 500

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)




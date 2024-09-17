from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openai import OpenAI
import os
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
CORS(app)

# Set up logging
if not app.debug:
    file_handler = RotatingFileHandler('canyon_portal.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

app.logger.setLevel(logging.INFO)
app.logger.info('Canyon Portal startup')

client = OpenAI(api_key="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")

@app.route('/')
def index():
    app.logger.info('Index page requested')
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_artifact():
    app.logger.info('Generate artifact request received')
    data = request.json
    raw_data = data['rawData']
    user_message = data['userMessage']
    
    app.logger.info(f'User message: {user_message}')
    app.logger.info(f'Raw data length: {len(raw_data)}')

    try:
        app.logger.info('Sending request to OpenAI')
        response = client.chat.completions.create(
            model="ft:gpt-3.5-turbo-0125:techhalo-labs:canyon-portal-poc1:A7DPjrcL",  # fine-tuned model ID
            messages=[
                {"role": "system", "content": "You are an AI assistant that helps create project artifacts. Use the provided raw data to inform your responses. Always make sure your responses are neatly formatted and presented to the user."},
                {"role": "user", "content": f"Raw data: {raw_data}\n\nUser message: {user_message}"}
            ],
            temperature=0.5
        )
        
        generated_artifact = response.choices[0].message.content
        app.logger.info('Artifact generated successfully')
        return jsonify({"artifact": generated_artifact}), 200
    except Exception as e:
        app.logger.error(f'Error generating artifact: {str(e)}', exc_info=True)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
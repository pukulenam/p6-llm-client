from flask import Flask, request, jsonify, render_template
import openai
import os
from dotenv import load_dotenv
from functools import wraps

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)

# Load OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Make sure the environment variable is set
if not openai.api_key:
  raise RuntimeError("Missing environment variable: OPENAI_API_KEY")

def api_key_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    api_key = request.args.get('api_key')
    if not api_key or api_key != os.getenv("API_KEY_SECRET"):  # Replace with your actual secret key
      return jsonify({'error': 'Unauthorized: Missing or invalid API key'}), 401

    return f(*args, **kwargs)

  return decorated_function

@app.route('/')
@api_key_required
def index():
  return render_template('index.html')

@app.route('/chat', methods=['POST'])
@api_key_required
def chat():
  data = request.json
  user_message = data.get('message')
  client = openai.OpenAI(api_key=openai.api_key)

  try:
    response = client.chat.completions.create(
      model="gpt-3.5-turbo",  # or your fine-tuned model name
      messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_message}
      ],
      max_tokens=150,
      temperature=0.7
    )

    reply = response.choices[0].message.content
    return jsonify({"reply": reply})

  except Exception as e:
    return jsonify({"error": str(e)})

if __name__ == '__main__':
  app.run(debug=True, port=15804, host='0.0.0.0')

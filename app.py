from flask import Flask, request, jsonify, render_template
import openai
import kode  # Import the secret module to access the API key

app = Flask(__name__)

# Set your OpenAI API key from secret.py
openai.api_key = kode.api_key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    client = openai.OpenAI(api_key=kode.api_key)

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
    app.run(debug=True)

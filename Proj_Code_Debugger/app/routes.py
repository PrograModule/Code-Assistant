from flask import Blueprint, render_template, request, jsonify
import openai

app_routes = Blueprint('app_routes', __name__)

# Load your OpenAI API key
openai.api_key = "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"

@app_routes.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        code = request.form.get("code")
        mode = request.form.get("mode")
        
        if mode == "debug":
            prompt = f"Debug the following Python code:\n\n{code}\n\nProvide clear explanations for any fixes."
        elif mode == "tutor":
            prompt = f"Explain what the following Python code does, step by step:\n\n{code}"
        else:
            return jsonify({"error": "Invalid mode selected."})

        try:
            response = openai.ChatCompletion.create(
            model="gpt-4",  # Replace with "gpt-4" if needed
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Explain what the following Python code does step by step:"}
            ],
            max_tokens=100,
            temperature=0.5
            )
            print(response["choices"][0]["message"]["content"].strip())

        except Exception as e:
            return jsonify({"error": str(e)})

    return render_template("index1.html")

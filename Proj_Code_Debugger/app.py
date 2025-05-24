import openai
from flask import Flask, request, render_template
from dotenv import find_dotenv, load_dotenv
import os

# Initialize Flask app
app = Flask(__name__)

# Store debugging history (temporary storage for demo)
debugging_history = []

# Store explanation history (temporary storage for demo)
explanation_history = []

# load the .env file
load_dotenv()
client = openai.OpenAI()
# Function to debug code snippets
def debug_code_snippet(code_snippet):
     
    try:
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=f"Debug the following Python code:\n\n{code_snippet}",
            # messages=[
            #     {"role": "system", "content": "You are a helpful assistant for debugging Python code."},
            #     {"role": "user", "content": f"Debug the following Python code:\n\n{code_snippet}"}
            # ],
            max_tokens=500,
            temperature=0.5
        )
        print(response.choices[0].text.strip())
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {e}"
    # Function to explain code logic, syntax, and design patterns
def explain_code_logic(code_snippet):
    try:
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=f"Explain the logic, syntax, and design patterns used in the following Python code:\n\n{code_snippet}",
            max_tokens=200,
            temperature=0.5
        )
        result = response.choices[0].text.strip()
        print(result)
        return result
    except Exception as e:
        return f"Error: {e}"

# Function to provide tutoring resources
def provide_tutoring_resources(topic):
    try:
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=f"Provide coding challenges and step-by-step lessons for the following topic:\n\n{topic}",
            max_tokens=500,
            temperature=0.5
        )
        result = response.choices[0].text.strip()
        print(result)
        return result
    except Exception as e:
        return f"Error: {e}"


# Function to suggest optimizations for code
def suggest_optimizations(code_snippet, language):
    try:
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=f"Suggest optimizations for the following {language} code. Include better algorithms, cleaner design patterns and provide the optimized version of given code:\n\n{code_snippet}",
            max_tokens=500,
            temperature=0.5
        )
        result = response.choices[0].text.strip()
        return result
    except Exception as e:
        return f"Error: {e}"

# Route for the index1 page
@app.route("/")
def index():
    return render_template("index1.html")

# @app.route("/debugger.html")
# def debugger1():
#     return render_template("debugger.html")


@app.route("/debugger.html")
def debugger():
    return render_template("debugger.html",debugging_history=debugging_history)


# Route to handle debugging
# @app.route("/debug", methods=["POST"])
# def debug():
#     code_snippet = request.form.get("code_snippet")
#     if not code_snippet:
#         return "Please provide a code snippet to debug."
#     debug_result = debug_code_snippet(code_snippet)
#     return render_template("debugger.html", code_snippet=code_snippet, debug_result=debug_result)
@app.route("/debug", methods=["POST"])
def debug():
    code_snippet = request.form.get("code_snippet")
    if not code_snippet:
        return "Please provide a code snippet to debug."

    debug_result = debug_code_snippet(code_snippet)  # This function should return full debugging details

    # Save the full debug session
    session_id = len(debugging_history) + 1
    debugging_history.append({"id": session_id, "summary": debug_result[:100], "full_debugging": debug_result})

    return render_template("debugger.html", 
                           code_snippet=code_snippet, 
                           debug_result=debug_result, 
                           debugging_history=debugging_history)

@app.route("/view_debug_report/<int:session_id>")
def view_debug_report(session_id):
    session = next((s for s in debugging_history if s["id"] == session_id), None)
    if session:
        return f"""
        <html>
        <head>
            <title>Debugging Report #{session_id}</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body class="container mt-5">
            <h1 class="mb-4">Debugging Report #{session_id}</h1>
            <pre class="bg-light p-3 border rounded">{session['full_debugging']}</pre>
            <a href="/debugger.html" class="btn btn-primary mt-3">Back to Debugger</a>
        </body>
        </html>
        """
    return "Report not found", 404


@app.route("/explainer")
def explainer():
    return render_template("explainer.html")

@app.route("/explainer.html")
def explainer1():
    return render_template("explainer.html")


# Route to handle explanation
@app.route("/explain", methods=["POST"])
def explain():
    code_snippet = request.form.get("code_snippet")
    if not code_snippet:
        return "Please provide a code snippet to explain."

    explanation_result = explain_code_logic(code_snippet)

    # Save the full explanation session
    session_id = len(explanation_history) + 1
    explanation_history.append({"id": session_id, "summary": explanation_result[:100], "full_explanation": explanation_result})

    return render_template("explainer.html", 
                           code_snippet=code_snippet, 
                           explanation_result=explanation_result, 
                           explanation_history=explanation_history)

@app.route("/view_explanation_report/<int:session_id>")
def view_explanation_report(session_id):
    session = next((s for s in explanation_history if s["id"] == session_id), None)
    if session:
        return f"""
        <html>
        <head>
            <title>Explanation Report #{session_id}</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body class="container mt-5">
            <h1 class="mb-4">Explanation Report #{session_id}</h1>
            <pre class="bg-light p-3 border rounded">{session['full_explanation']}</pre>
            <a href="/explainer" class="btn btn-primary mt-3">Back to Explainer</a>
        </body>
        </html>
        """
    return "Report not found", 404


@app.route("/tutoring")
def tutor():
    return render_template("tutoring.html")

# @app.route("/tutoring")
# def tutor1():
#     return render_template("tutoring.html")
# @app.route("/tutoring")
# def tutor2():
#     return render_template("tutoring.html")
# Route to handle tutoring resources
@app.route("/tutoring", methods=["POST"])
def tutoring():
    topic = request.form.get("topic")
    if not topic:
        return "Please provide a topic for tutoring resources."

    tutoring_resources = provide_tutoring_resources(topic)

    return render_template("tutoring.html", topic=topic, tutoring_resources=tutoring_resources)

@app.route("/optimizer")
def optimizer():
    return render_template("optimizer.html")

# Route to handle optimizations
@app.route("/optimize", methods=["POST"])
def optimize():
    code_snippet = request.form.get("code_snippet")
    language = request.form.get("language")
    if not code_snippet or not language:
        return "Please provide both a code snippet and a programming language to suggest optimizations."
    
    optimization_result = suggest_optimizations(code_snippet, language)
    return render_template(
        "optimizer.html",
        code_snippet=code_snippet,
        language=language,
        optimization_result=optimization_result
    )

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        print(f"Received message from {name} ({email}): {message}")  
        return "Thank you for contacting us!"
    return render_template("contact.html")

@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)


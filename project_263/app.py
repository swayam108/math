from flask import Flask, render_template, request
import requests
import urllib.parse  # For URL encoding

app = Flask(__name__)

@app.route('/')
def main():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def maths_operations():
    equation = request.form['text']
    operation = request.form['operation']

    # Generate the appropriate URL based on the operation
    if operation == 'simplify':
        result_url = f'http://api.mathjs.org/v4/?expr={urllib.parse.quote(equation)}'
    elif operation == 'factors':
        result_url = f'http://api.mathjs.org/v4/?expr=factor({urllib.parse.quote(equation)})'
    else:
        return render_template("index.html", result="Invalid operation", equation=equation)

    print(f"Generated URL: {result_url}")  # Debugging output

    # Make the request to Math.js API
    response = requests.get(result_url)

    if response.status_code == 200:
        answer = response.text  # Math.js returns plain text
    else:
        answer = f"Error: Received status code {response.status_code}"

    return render_template("index.html", result=answer, equation=equation)

if __name__ == "__main__":
    app.run()

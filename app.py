from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome to the Grade Submission and Viewing System!'

if __name__ == '__main__':
    app.run(debug=True)

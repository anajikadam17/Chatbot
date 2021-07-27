from flask import Flask, render_template, request
import main
import test
import Response

app = Flask(__name__)


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/get')
def get_bot_response():
    userText = request.args.get('msg')
    print(userText)
    return main.chatbot_response(str(userText))

@app.route('/get1')
def get_bot_response1():
    userText = request.args.get('msg')
    print(userText)
    resp, tag = test.response(str(userText))
    print(tag)
    if tag in ["vegMenu","nonVegMenu"]:
        message = Response.imageResponce(resp, tag)
        return message
    message = Response.textResponce(resp)
    return message

if __name__ == '__main__':
    app.run(debug=True)

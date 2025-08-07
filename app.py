from flask import Flask, render_template, request, redirect, url_for
import os
from whatsapptools import WhatsAppDriver

app = Flask(__name__, template_folder='Templates', static_folder='static', static_url_path='/')
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'img')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


@app.route('/')
def home():
    return "Flask is running. Click <a href='/send'>here</a> to send WhatsApp messages."


@app.route('/send')
def send_messages():
    numbers = ["7406073514", "6235305505"]
    message = "Hello from Flask triggered WhatsApp automation!"
    wts = WhatsAppDriver()
    for number in numbers:
        wts.send_message_to_contact(number, message)
    return "Done sending messages!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

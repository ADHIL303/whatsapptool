from flask import Flask, render_template, request, redirect, url_for,session
from flask_sqlalchemy import SQLAlchemy
import os
from whatsapptools import WhatsAppDriver  # This is your Selenium automation
from sqlalchemy import and_
# ------------------- Flask Setup ------------------- #
app = Flask(__name__, template_folder='Templates', static_folder='static', static_url_path='/')
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'img')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'devsecret')  # fallback value

# ------------------- DB Config ------------------- #
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///numbers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ------------------- DB Model ------------------- #
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_title = db.Column(db.String(100))
    category = db.Column(db.String(50))
    username = db.Column(db.String(50))
    phone = db.Column(db.String(20), unique=True)

# ------------------- Routes ------------------- #
@app.route('/')
def home():
    return render_template("index.html")
@app.route('/contacts', methods=['GET', 'POST'])
def show_contacts():
    # Fetch distinct filter values
    categories = [c[0] for c in Contact.query.with_entities(Contact.category).distinct().all()]
    usernames = [u[0] for u in Contact.query.with_entities(Contact.username).distinct().all()]
    titles = [t[0] for t in Contact.query.with_entities(Contact.group_title).distinct().all()]

    # Initialize filter selections and contact list
    selected_category = ''
    selected_username = ''
    selected_title = ''
    contacts = Contact.query.all()  # Default - all contacts

    if request.method == 'POST':
        selected_category = request.form.get('category', '')
        selected_username = request.form.get('username', '')
        selected_title = request.form.get('title', '')
        action = request.form.get('action')

        # Build filter query
        query = Contact.query
        if selected_category:
            query = query.filter_by(category=selected_category)
        if selected_username:
            query = query.filter_by(username=selected_username)
        if selected_title:
            query = query.filter_by(group_title=selected_title)

        if action == 'filter':
            # Just filter and show
            contacts = query.all()

        elif action == 'send':
            WhatsAppDriver.login()
            # Send messages to filtered
            filtered_numbers = query.with_entities(Contact.phone).distinct().all()
            numbers = [n[0] for n in filtered_numbers]

            if not numbers:
                return "❌ No numbers to send to."

            message = "Hello from Flask triggered WhatsApp automation!"
            wts = WhatsAppDriver()

            for number in numbers:
                try:
                    wts.send_message_to_contact(number, message)
                except Exception as e:
                    print(f"❌ Failed for {number}: {e}")

            return f"✅ Tried sending to {len(numbers)} numbers."

    # Render template with filters and contact list
    return render_template(
        'contacts.html',
        contacts=contacts,
        categories=categories,
        usernames=usernames,
        titles=titles,
        selected_category=selected_category,
        selected_username=selected_username,
        selected_title=selected_title
    )


@app.route('/collect', methods=['GET', 'POST'])
def collect_number():
    if request.method == 'POST':
        group_title = request.form['group_title']
        category = request.form['category']
        username = request.form['username']

        w = WhatsAppDriver()
        numbers = w.collect_numbers_from_whatsapp(title=group_title)

        for num in numbers:
            if not Contact.query.filter_by(phone=num).first():
                contact = Contact(
                    group_title=group_title,
                    category=category,
                    username=username,
                    phone=num
                )
                db.session.add(contact)

        db.session.commit()
        return f"✅ Collected and saved {len(numbers)} numbers from '{group_title}'"
    
    return render_template('collect.html')

@app.route('/send')
def send_messages():
    numbers = session.get('filtered_numbers', [])

    if not numbers:
        return "❌ No numbers to send to."

    message = "Hello from Flask triggered WhatsApp automation!"
    wts = WhatsAppDriver()

    for number in numbers:
        try:
            wts.send_message_to_contact(number, message)
        except Exception as e:
            print(f"❌ Failed for {number}: {e}")
    
    return f"✅ Tried sending to {len(numbers)} numbers."


# ------------------- Main ------------------- #
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Conversation
from app import db
from app.forms import LoginForm, RegistrationForm
from app.gpt import get_gpt_response
import os
from flask import request, redirect, url_for, render_template
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.models import Conversation
from app import db
from app.gpt import get_gpt_response, retrieve_relevant_content

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    user_chats = Conversation.query.filter_by(user_id=current_user.id).group_by(Conversation.title).all()
    chat_id = request.args.get('chat_id')
    selected_chat = Conversation.query.filter_by(id=chat_id, user_id=current_user.id).all() if chat_id else []

    if request.method == 'POST':
        user_message = request.form['message']
        chat_title = request.form.get('title', 'Untitled Chat')
        rag_enabled = 'rag_enabled' in request.form

        retrieved_content = ''
        if rag_enabled and 'file' in request.files:
            file = request.files['file']
            if file and file.filename:
                filepath = secure_filename(file.filename)
                filepath = os.path.join('uploads', filepath)
                file.save(filepath)

                # Retrieve relevant content from the file
                retrieved_content = retrieve_relevant_content(filepath, user_message)

        # Generate response using retrieved content
        gpt_response = get_gpt_response(user_message, retrieved_content)

        conversation = Conversation(user_id=current_user.id, title=chat_title, message=user_message, response=gpt_response)
        db.session.add(conversation)
        db.session.commit()

        return redirect(url_for('main.chat', chat_id=conversation.id))

    return render_template('chat.html', user_chats=user_chats, selected_chat=selected_chat)


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('main.chat'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully! Please log in.')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))



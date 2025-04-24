from flask_socketio import emit
from flask_login import current_user
from . import socketio
from .gpt import get_gpt_response
from .models import Conversation, db

@socketio.on('send_message')
def handle_message(data):
    user_message = data.get('message')
    if not current_user.is_authenticated:
        emit('receive_message', {'error': 'User not authenticated'})
        return
    
    # Get GPT response
    gpt_response = get_gpt_response(user_message)
    
    # Save to DB
    conversation = Conversation(user_id=current_user.id, message=user_message, response=gpt_response)
    db.session.add(conversation)
    db.session.commit()
    
    # Emit response back
    emit('receive_message', {
        'user_message': user_message,
        'gpt_response': gpt_response
    }, broadcast=True)

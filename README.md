# Chat with GPT and RAG

This project is a Flask-based web application that allows users to interact with GPT models and utilize Retrieval-Augmented Generation (RAG) capabilities. Users can log in, chat with a GPT model, upload files to retrieve relevant content, and engage in personalized conversations. The application uses Flask-Login for user authentication and integrates GPT responses for dynamic conversation flow.

## Features

- **User Authentication**: Users can register, log in, and log out using Flask-Login.
- **Chat with GPT**: Users can chat with a GPT model, which generates responses based on the user's input.
- **Retrieval-Augmented Generation (RAG)**: Users can upload files, and the application will retrieve relevant content from them to augment the GPT response.
- **Conversation History**: Conversations are stored in a database, and users can view their previous chats.

## Technologies Used

- **Flask**: A lightweight Python web framework used for building the application.
- **Flask-Login**: Provides user session management and authentication.
- **SQLAlchemy**: ORM for managing the database.
- **Jinja2**: Template engine used for rendering HTML templates.
- **GPT-3/GPT-2**: Generative Pretrained Transformers for generating responses based on user inputs.
- **Werkzeug**: Utility library for handling file uploads and secure filenames.

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Hmishra230/Chat-with-GPT-and-RAG.git
cd Chat-with-GPT-and-RAG

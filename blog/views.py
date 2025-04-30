from django.shortcuts import render
from django.http import HttpResponse
from .models import ConversationPair, UnknownQuestion
import os
import spacy
nlp = spacy.load('en_core_web_sm')
from .models import SimplifierMapping


# Create your views here.
# What user gonna see.

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer


# Create chatbot instance with logic adapters
bot = ChatBot(
    'chatbot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',  # Stores data in a SQL database
    database_uri='sqlite:///db.sqlite3',  # Path to the local SQLite database
    read_only=False,  # Allows the bot to learn during conversation 
    
    logic_adapters=[  # Logic that controls how the bot decides what to respond
        {
            'import_path': 'chatterbot.logic.BestMatch',  # Chooses the best matching response
            'default_response': "Sorry, I don't know that yet. I'm still learning!",  # Fallback if no good match found
            'maximum_similarity_threshold': 0.98  # Only respond if match is 98% or higher
        },
    ]
)



# Train the bot using built-in ChatterBot corpus data
corpus_trainer = ChatterBotCorpusTrainer(bot)
try:
    corpus_trainer.train(
        "chatterbot.corpus.english.greetings", # Predefined greetings dataset
        "chatterbot.corpus.english.conversations" # Predefined small talk and conversations
    )
except Exception as e:
    print(f"Corpus training failed: {e}")



# Lemmatization function using spaCy
def lemmatize_input(text):
    doc = nlp(text)  # Process the text using spaCy's language model
    return " ".join([token.lemma_ for token in doc])  # Join all lemmatized tokens into a single string



# Smart simplifier: rewrites complex words into friendly terms
def simplify_response(text):
    mappings = SimplifierMapping.objects.all()

    for mapping in mappings:
        if mapping.keyword.lower() in text.lower():
            text = text.replace(mapping.keyword, mapping.replacement)

    return text



# Custom training function to train the bot using multiple .txt files
def train_bot_from_files():
    list_trainer = ListTrainer(bot)  # Initialize ChatterBot's list-based trainer

    # List of training data files (each contains Q&A pairs)
    training_files = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '../random_data.txt'),       # General casual or chit-chat
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '../python_data.txt'), # Python Q&A - Part 1
    ]

    # Loop through each file and train the bot line-by-line
    for file_path in training_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]  # Remove blank lines
            list_trainer.train(lines)  # Train the bot with each cleaned line

# Call the function once when server starts
train_bot_from_files()



# Retrains the bot using Q&A data stored in the database
def retrain_bot_from_conversations():
    all_pairs = ConversationPair.objects.all()  # Fetch all saved Q&A pairs
    training_data = []

    # Add each question-answer pair to the training list
    for pair in all_pairs:
        training_data.append(pair.question)
        training_data.append(pair.answer)

    # Train only if there is data
    if training_data:
        trainer = ListTrainer(bot)  # Initialize the trainer
        trainer.train(training_data)  # Train bot with dynamic Q&A data from the database



def retrain_now(request):
    retrain_bot_from_conversations()
    return HttpResponse("Bot retrained from database!")



def index(request):
    return render(request, 'blog/index.html')



def specific(request):
    return HttpResponse("This is specific url")



# View to handle user input and return chatbot response
def getResponse(request): 
    userMessage = request.GET.get('userMessage')  # Get user message from the frontend

    # Get the chatbot's response using ChatterBot
    chatResponse = str(bot.get_response(userMessage))

    # Apply smart simplification
    simplifiedResponse = simplify_response(chatResponse)

    # Log unknown questions into the database for manual review/training
    if "Sorry, I don't know that yet" in chatResponse:
        if not UnknownQuestion.objects.filter(question=userMessage).exists():
            UnknownQuestion.objects.create(question=userMessage)

    # Send final response back to the frontend
    return HttpResponse(simplifiedResponse)

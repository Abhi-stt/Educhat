import os
import re  # Added for formatting
import google.generativeai as genai
from dotenv import load_dotenv
from flask import Flask, request, render_template_string

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key='AIzaSyBcZbAUdmRInxr7ZHvqIic7JaOpqTCo5-w')
# print(genai.list_models())

models = genai.list_models()
for m in models:
    print(m.name, m.supported_generation_methods)

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-pro-latest')

app = Flask(__name__)  

# Subject-specific prompts
SUBJECT_PROMPTS = {
    "physics": (
        "You are a Physics expert assistant. ONLY answer questions that are strictly related to physics topics like "
        "classical mechanics, quantum physics, thermodynamics, and relativity. If the user's question is not related to physics, "
        "respond politely with: 'Please ask only Physics-related questions.'"
    ),
    "chemistry": (
        "You are a Chemistry expert assistant. ONLY answer questions that are strictly related to chemistry topics including "
        "organic, inorganic, physical, and biochemistry. If the user's question is not about chemistry, respond with: "
        "'Please ask only Chemistry-related questions.'"
    ),
    "philosophy": (
        "You are a Philosophy expert assistant. ONLY answer questions about philosophy: metaphysics, epistemology, ethics, logic, "
        "and related philosophers. If the user's question is unrelated to philosophy, respond with: "
        "'Please ask only Philosophy-related questions.'"
    )
}


HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>EduChat - Subject Expert</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            max-width: 800px; 
            margin: 0 auto; 
            padding: 20px;
            background-color: #f5f7fa;
        }
        .welcome-message {
            background-color: #4285f4;
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
        }
        .subject-options {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            justify-content: center;
            margin: 20px 0;
        }
        .subject-btn {
            background-color: #34a853;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            transition: all 0.3s;
        }
        .subject-btn:hover {
            background-color: #2d8e47;
            transform: translateY(-2px);
        }
        .chat-container { 
            border: 1px solid #ddd; 
            border-radius: 5px; 
            height: 400px; 
            overflow-y: scroll; 
            padding: 15px; 
            margin-bottom: 15px;
            background-color: white;
        }
        .user-message { 
            background-color: #e3f2fd; 
            padding: 10px; 
            border-radius: 8px; 
            margin: 8px 0;
            max-width: 80%;
            margin-left: auto;
        }
        .bot-message { 
            background-color: #f1f3f4; 
            padding: 10px; 
            border-radius: 8px; 
            margin: 8px 0;
            max-width: 80%;
        }
        .input-area {
            display: flex;
            gap: 10px;
        }
        input[type="text"] { 
            flex: 1; 
            padding: 10px; 
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }
        button[type="submit"] { 
            background-color: #4285f4;
            color: white;
            border: none;
            padding: 0 20px;
            border-radius: 5px;
            cursor: pointer;
        }
        .change-subject {
            display: inline-block;
            margin-top: 15px;
            color: #4285f4;
            text-decoration: none;
        }
    </style>
</head>
<body>
    {% if not subject %}
    <div class="welcome-message">
        <h2>Hi! I am EduChat</h2>
        <p>I can help you with subjects like Physics, Chemistry, and Philosophy</p>
    </div>
    
    <div class="subject-options">
        <form method="POST">
            <button class="subject-btn" name="subject" value="physics">Physics</button>
            <button class="subject-btn" name="subject" value="chemistry">Chemistry</button>
            <button class="subject-btn" name="subject" value="philosophy">Philosophy</button>
        </form>
    </div>
    {% else %}
    <h2 style="color: #4285f4;">{{ subject|capitalize }} Expert</h2>
    <div class="chat-container">
        <div class="bot-message">
            Welcome to the {{ subject }} expert chat! How can I help you with {{ subject }} today?
        </div>
        {% for msg in conversation %}
        <div class="{{ 'user' if msg.role == 'You' else 'bot' }}-message">
            {% if msg.role == 'You' %}
            <strong>{{ msg.role }}:</strong> {{ msg.content|safe }}
            {% else %}
            {{ msg.content|safe }}
            {% endif %}
        </div>
        {% endfor %}
    </div>
    <form method="POST" class="input-area">
        <input type="hidden" name="subject" value="{{ subject }}">
        <input type="text" name="query" autocomplete="off" autofocus placeholder="Ask your {{ subject }} question...">
        <button type="submit">Send</button>
    </form>
    <a href="/" class="change-subject">← Choose another subject</a>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def chat():
    subject = request.form.get('subject')
    query = request.form.get('query', '').strip()
    
    conversation = []
    
    if subject:
        if not query:  # First entry to subject
            pass  # Welcome message is handled in template
        else:
            # Add user message to conversation
            conversation.append({
                'role': 'You',
                'content': query
            })
            
            # Generate response with subject-specific context
            try:
                response = model.generate_content(
                    f"{SUBJECT_PROMPTS[subject]}\n\nUser question: {query}\n\n"
                    "IMPORTANT: Do NOT answer questions outside this subject area. If the question is not related, politely decline."
                )
                bot_response = response.text

                # Convert **bolds** to <strong> tags
                bot_response = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', bot_response)
                
                # Replace * bullets with • for cleaner bullet points
                bot_response = bot_response.replace('* ', '• ')

                # Split into lines for line-by-line display
                bot_response_lines = bot_response.strip().split('\n')
            except Exception as e:
                bot_response_lines = [f"Sorry, I encountered an error: {str(e)}"]

            # Add each line as a separate message (no Bot label)
            for line in bot_response_lines:
                if line.strip():
                    conversation.append({
                        'role': 'Bot',
                        'content': line.strip()
                    })
    
    return render_template_string(HTML_TEMPLATE, 
                               subject=subject, 
                               conversation=conversation)

if __name__ == '__main__':  
    app.run(debug=True)

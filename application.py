from flask import Flask, render_template, request
import sys
from  chatbot import Chatbot
from common import model
from characters import system_role, instruction
import atexit

simsim = Chatbot(
    model=model.basic,
    system_role=system_role,
    instruction=instruction,
    user = "유빈",
    assistant = "심심이"
    )


application = Flask(__name__)

@application.route("/chat-app")
def chat_app():
    return render_template('chat.html')

# JSON data
@application.route('/chat-api', methods=['POST'])
def chat_api():
    request_message = request.json['request_message']
    print("request_message:", request_message)
    simsim.add_user_message(request_message)
    response = simsim.send_request()
    simsim.add_response(response)
    response_message = simsim.get_response_content()
    simsim.handle_token_limit(response)
    simsim.clean_context()
    print("response_message:", response_message)
    return {"response_message": response_message}

@atexit.register
def shutdown():
    print("flask shutting down...")
    simsim.save_chat()

# cd chapter13
# python application.py 80
# http://127.0.0.1/chat-app
if __name__ == "__main__":
    application.run(debug=True, host='0.0.0.0', port=int(sys.argv[1]))
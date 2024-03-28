__author__ = "Karar Shah"
__email__ = "karar.shah2015@gmail.com"

import argparse
from flask import Flask, request, jsonify
import datetime
from openai import OpenAI

# Helper function
def call_gpt(user_input, prompt, api_key, model="gpt-3.5-turbo", temperature=0.5):
    """
    Generate a response using the OpenAI model.

    Parameters:
        user_input (str): The user's input/query.
        prompt (str): The initial prompt to start the conversation.
        api_key (str): The API key for accessing the OpenAI service.
        model (str, optional): The model to use for generation. Defaults to "gpt-3.5-turbo".
        temperature (float, optional): Controls the randomness of the response. Higher values make the response more diverse. Defaults to 0.5.

    Returns:
        str: The generated response from the model.
    """
    # Initialize the OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Generate completion using the provided user input and prompt
    completion = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input}
        ]
    )
    # Return the response content
    return completion.choices[0].message.content

# Function for route 1
def text_to_text(user_input, api_key):
    """
    Generate a response to the user's input/question using the OpenAI GPT-3.5 model.

    Parameters:
        user_input (str): The user's input/query.
        api_key (str): The API key for accessing the OpenAI service.


    Returns:
        str: The generated response from the GPT-3.5 model.
    """
    try:
        # Get the current date and time
        current_datetime = datetime.datetime.now()
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M")

        # Create the prompt including the current date and time
        TTT_prompt = f"""You are a helpful assistant who responds to anything asked. Current date time is {current_datetime}"""
        
        # Generate response using the call_gpt function
        resp = call_gpt(user_input, TTT_prompt, api_key)
        
        # Return the generated response
        return resp
    except Exception as e:
        return f"An error occurred while processing your request from OpenAi: {str(e)}"

# Function for route 2
def translate(user_input, api_key):
    """
    Translate the provided text into the specified language using the OpenAI GPT-3.5 model.

    Parameters:
        user_input (str): The user's input/query specifying the translation request.
        api_key (str): The API key for accessing the OpenAI service.
    Returns:
        str: The translated text.
    """
    try:
        # Create the prompt for translation including instructions
        Translation_prompt = f"""
        You are a helpful assistant who accurately translates the given text into the mentioned language.

        For the provided text, you perform the following actions: 
        1 - Translate the text delimited by triple backticks into the language mentioned in the 'user' message
        2 - Output the result in the following format
        Translation from <input language name> to <target language name>.
        Translation: <put the translated results here>
        """
        
        # Generate response using the call_gpt function
        resp = call_gpt(user_input, Translation_prompt, api_key)
        
        # Return the generated response
        return resp
    except Exception as e:
        return f"An error occurred while processing your request from OpenAi: {str(e)}"

# Function for route 3
def computation(user_input, api_key):
    """
    Perform mathematical and computation-related tasks using the OpenAI GPT-3.5 model.

    Parameters:
        user_input (str): The user's input/query specifying the computational task.
        api_key (str): The API key for accessing the OpenAI service.
    Returns:
        str: The computed results.
    """
    try:
        # Get the current date and time
        current_datetime = datetime.datetime.now()
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M")

        # Create the prompt for computation including instructions and current date and time
        computation_prompt = f""" 
        You are a helpful assistant proficient in mathematics and computation-related tasks. The current date and time are {current_datetime}.
        You will be given computational tasks that may involve various calculations such as algebraic operations or time computations.
        Your objective is to accurately compute the results for each given task separately. This may entail performing algebraic calculations, manipulating data with time considerations, or other computational tasks as required.
        Ensure precision in your calculations for each task and provide the results or intermediate steps as necessary.
        """
        
        # Generate response using the call_gpt function
        resp = call_gpt(user_input, computation_prompt, api_key,temperature=0)
        
        # Return the generated response
        return resp
    except Exception as e:
        return f"An error occurred while processing your request from OpenAi: {str(e)}"
    
# Parse arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Run Flask app with OpenAI parameters.")
    parser.add_argument("--openai_api_key", required=True, help="OpenAI API key")
    parser.add_argument("--auth_token", default="access_token_to_this_server", help="Authentication token")
    return parser.parse_args()

app = Flask(__name__)

# Route 1: Text-to-Text
@app.route("/text", methods=["POST"])
def handle_text_to_text():
    request_data = request.get_json()
    auth_token = request_data.get("verify_token")
    if auth_token != args.auth_token:
        return jsonify({"error": "Invalid authentication token"}), 401

    user_input = request_data.get("user_input", "")
    response = text_to_text(user_input, args.openai_api_key)
    return jsonify({"response": response})


# Route 2: Translate
@app.route("/translate", methods=["POST"])
def handle_translate():
    request_data = request.get_json()
    auth_token = request_data.get("verify_token")
    if auth_token != args.auth_token:
        return jsonify({"error": "Invalid authentication token"}), 401
    
    user_input = request_data.get("user_input", "")
    response = translate(user_input,  args.openai_api_key)
    return jsonify({"response": response})


# Route 3: Computation
@app.route("/computate", methods=["POST"])
def handle_computation():
    request_data = request.get_json()
    auth_token = request_data.get("verify_token")
    if auth_token != args.auth_token:
        return jsonify({"error": "Invalid authentication token"}), 401
    
    user_input = request_data.get("user_input", "")
    response = computation(user_input,  args.openai_api_key)
    return jsonify({"response": response})


if __name__ == "__main__":
    args = parse_arguments()
    app.run(host="0.0.0.0", port=8008, threaded=True)

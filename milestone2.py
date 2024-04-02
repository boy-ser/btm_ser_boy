__author__ = "Karar Shah"
__email__ = "karar.shah2015@gmail.com"

import argparse
from flask import Flask, request, jsonify
import datetime
from openai import OpenAI
import requests
import time


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
    
# Function for route 4
def post_data(api_key, prompt, aspect_ratio, process_mode):
    """
    Send a POST request to the Midjourney API endpoint to process an image based on the provided prompt.

    Parameters:
        api_key (str): The API key for accessing the Midjourney API.
        prompt (str): The prompt to guide the image processing.
        aspect_ratio (str): The aspect ratio for the output image.
        process_mode (str): The mode for processing the image.

    Returns:
        dict or None: A dictionary containing the response data if the request was successful, otherwise None.
    """
    # Define the endpoint URL
    endpoint = "https://api.midjourneyapi.xyz/mj/v2/imagine"

    # Set the headers with the API key
    headers = {
        "X-API-KEY": api_key
    }
    
    # Set the data payload
    data = {
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "process_mode": process_mode,
    }

    # Send the POST request
    response = requests.post(endpoint, headers=headers, json=data)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Return the response content as a dictionary
        return response.json()
    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code} - {response.text}")
        return None

def get_message(task_id):
    """
    Retrieve a message from the Midjourney API based on the provided task ID.

    Parameters:
        task_id (str): The ID of the task/message to retrieve.

    Returns:
        dict or None: A dictionary containing the retrieved message if the request was successful, otherwise None.
    """
    # Define the endpoint URL
    endpoint = "https://api.midjourneyapi.xyz/mj/v2/fetch"
    
    # Set the data payload
    data = {
        "task_id": task_id
    } 

    # Send the POST request
    response = requests.post(endpoint, json=data)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Return the response content as a dictionary
        return response.json()
    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code} - {response.text}")
        return None

def text_to_image(api_key, prompt, aspect_ratio='1:1', process_mode='fast'):
    """
    Convert text to an image using the Midjourney API.

    Parameters:
        api_key (str): The API key for accessing the Midjourney API.
        prompt (str): The prompt to guide the image creation.
        aspect_ratio (str, optional): The aspect ratio for the output image. Defaults to '1:1'.
        process_mode (str, optional): The mode for processing the image. Defaults to 'fast'.

    Returns:
        dict or str: A dictionary containing the image URL and additional data if the conversion was successful,
                    or a string indicating failure if the conversion was unsuccessful.
    """
    # Send a POST request to initiate image creation
    response_data = post_data(api_key, prompt, aspect_ratio, process_mode)
    
    # Check if the response is successful and contains necessary data
    if response_data and response_data['success'] == True:
        # Retrieve message content based on task ID
        message_content = get_message(response_data['task_id'])
        
        # Set initial wait time before checking status again
        wait_time = 40
        
        # Continue checking status until task is finished or failed
        while True:
            # If task failed, return an error message
            if message_content['status'] == 'failed':
                return 'The task execution failed.'
            else:
                # Wait for a certain time before checking status again
                time.sleep(wait_time)
                wait_time = 5
                
                # Retrieve message content again
                message_content = get_message(response_data['task_id'])
                
                # If task is finished, return image URL and additional data
                if message_content['status'] == 'finished':
                    return {'1image_url': message_content['task_result']['image_url'], '2data': message_content}







# Parse arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Run Flask app with OpenAI parameters.")
    parser.add_argument("--openai_api_key", required=True, help="API key")
    parser.add_argument("--mj_api_key", required=True, help="MidJouney API key")
    parser.add_argument("--auth_token", default="access_token_to_this_server", help="Authentication token")
    return parser.parse_args()

app = Flask(__name__)

# Route 1: Text-to-Text
@app.route("/text", methods=["POST"])
def handle_text_to_text():
    request_data = request.get_json()
    print('request_data',request_data)
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
    print('request_data',request_data)
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
    print('request_data',request_data)

    auth_token = request_data.get("verify_token")
    if auth_token != args.auth_token:
        return jsonify({"error": "Invalid authentication token"}), 401
    
    user_input = request_data.get("user_input", "")
    response = computation(user_input,  args.openai_api_key)
    return jsonify({"response": response})

# Route 4: Text to Image
# Text me -> __email__ = "karar.shah2015@gmail.com"
@app.route("/image", methods=["POST"])
def handle_image():
    request_data = request.get_json()
    print('request_data',request_data)

    auth_token = request_data.get("verify_token")
    if auth_token != args.auth_token:
        return jsonify({"error": "Invalid authentication token"}), 401
    
    user_input = request_data.get("user_input", "")
    response = text_to_image(args.mj_api_key, user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    args = parse_arguments()
    app.run(host="0.0.0.0", port=8008, threaded=True)

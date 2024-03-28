import requests
import json

url = "http://16.16.182.251/text"

auth_token = "hello"

# Example messages
# messages = "English to Kazakh, The square root of 3.14 is 1!"
# messages = "What is 3000 times 3000 divided by 1000?"
messages = "Who is the president of Kazakhstan?"
headers = {"Content-Type": "application/json"}


def send_request():
    response = requests.post(
        url, 
        data=json.dumps({"user_input": messages, "verify_token":auth_token}), 
        headers={"Content-Type": "application/json"}
    )
    print("Response:", response.json()["response"])

send_request()

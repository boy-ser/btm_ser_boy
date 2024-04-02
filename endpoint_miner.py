import os
import time
import argparse
import bittensor
from typing import List, Dict, Optional
import traceback
from datetime import datetime


import requests
import json

from prompting.baseminer.miner import Miner
from prompting.protocol import Prompting


class EndpointMiner(Miner):
    @classmethod
    def add_args(cls, parser: argparse.ArgumentParser):

        parser.add_argument( '--endpoint.verify_token', type=str, help='Auth' )
        parser.add_argument( '--endpoint.url', type=str, help='Endpoint' )

    def config(self) -> "bittensor.Config":

        parser = argparse.ArgumentParser(description="OpenAI Miner Configs")
        self.add_args(parser)
        return bittensor.config(parser)

    def __init__(self, *args, **kwargs):
        super(EndpointMiner, self).__init__(*args, **kwargs)
        print("Initialized")


    def prompt(self, synapse: Prompting) -> Prompting:

        
        start_time=time.time()
        errored=False
        
        generation=""
        
        error_msg = "None"
        try:
            messages = [
                {"role": role, "content": user_input}
                for role, user_input in zip(synapse.roles, synapse.messages)
            ]
            
            print("messages", messages)
            response = requests.post(self.config.endpoint.url, data=json.dumps({"messages": str(messages), "verify_token":self.config.endpoint.verify_token}), headers= {"Content-Type": "application/json"}, timeout=12)
            
            generation = response.json()["response"] 

        except Exception as e:
            traceback.print_exc()

            

        time_to_sleep = 9.6 - (time.time()-start_time)
        if time_to_sleep > 0:
            time.sleep(time_to_sleep)
            

        synapse.completion = generation
        
        print("messages:", messages)
        print("Generation:", generation)
        return synapse


if __name__ == "__main__":
    print("Starting")
    with EndpointMiner():
        while True:
            print("running...", time.time())
            time.sleep(10)
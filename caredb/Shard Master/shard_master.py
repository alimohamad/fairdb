from copy import deepcopy
from flask import Flask, request, jsonify
from math import ceil
from random import shuffle
import requests
import sys

app = Flask(__name__)

shard_servers = ["http://8007947f.ngrok.io/", "http://a1649ac0.ngrok.io/"]  # This is an empty array that will eventually be filled with the IPs of the individual shard servers.

@app.route('/', methods=['GET'])
def hello():
        return "yerrrrrr"

@app.route('/add', methods=['POST'])
def send_shards():
        r = request.get_json()  # This will contain the user id of a case manager, as well as a new document (encrypted).

        response = []

        encrypted_text = r['body']
        num_shards =  ceil(len(encrypted_text)/len(shard_servers))
        print("ENCRYPTED TEXT LEN:" , len(encrypted_text) , "NUM SERVERS:", len(shard_servers))
        shards = [encrypted_text[start:start+num_shards] for start in range(0, len(encrypted_text), num_shards)]
        
        print("SHARDS", shards)

        visited_nodes = deepcopy(shard_servers)
        count = 0
        for shard in shards:
                shuffle(visited_nodes)
                url = visited_nodes.pop() + "/new_shard"
                user_id = r['user_id']
                filename = r['case_id'] + "-" + str(count)
                count += 1
                
                resp = requests.post(url=url, data={'user_id': user_id, 'encrypted_content': shard, 'filename': filename})
                print(resp)

                response.append(resp.json())
        
        return jsonify({'files': response})


@app.route('/find', methods=['POST'])
def get_shards():
        r = request.get_json()  # This will contain the user id of the case manager, as well as the list of their cases.

        all_cases = {}  # Object being returned.

        shard_dump = []  # List of shard tuples from API requests.

        for server in shard_servers:
                #  Make POST request to shard server with specific IP with "requests" library to get shards. Add all shards to dump.
                shards = requests.post(url=server+"/retrieve", data={'user_id': r['user_id']}).json()
                shard_dump.extend(shards['response'])
        
        all_shards = remove_duplicates(shard_dump)  # Remove Duplicates
        
        for case in r['cases']:   
                relevant_shards = list(filter(lambda x: case in x[0], all_shards))  # Get shards relevant to given case.
                relevant_shards.sort(key=lambda x: x[0])  # Sort lexicographically (in numerical order).
                relevant_shards = map(lambda x: x[1].strip(), relevant_shards)  # Removes shard ids, just keeps shards to join them.

                print("RELEVANT: ", relevant_shards)

                # Join shards as one complete encrypted bytestring.
                s = ""
                reassembled_case = s.join(relevant_shards)

                # Append to return dictionary.
                all_cases[case] = reassembled_case
        
        return jsonify({'response': all_cases})

def remove_duplicates(shard_dump):  # Add to a set if not seen before. Seen, before, skip.
        seen = set()
        all_shards = [(a, b) for a, b in shard_dump if not (a in seen or seen.add(a))] 
        return all_shards

if __name__ == "__main__":
        app.run()




        
        
        
                
        
    
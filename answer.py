import requests
import json
import hashlib
import argparse
import sys

def get_token_input():
    try:
        arg = str(sys.argv[1])
        print('TOKEN passed: ' + arg)
        return(arg)
    except:
        e = sys.exc_info()[0]
        print(e)

def get_data(TOKEN) :
    auth_url = 'https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token=' + TOKEN
    receive = requests.get(auth_url)
    data = json.loads(receive.text)
    return data

def decode(string, shift):
    decoded = ''
    for letter in string:
        if letter.isalpha():
            decoded = decoded + chr(ord(letter) - shift)
        else :
            decoded = decoded + letter
    
    return(decoded)

def send_data(TOKEN):
    submit_url = 'https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token=' + TOKEN
    answer = {'answer': open('answer.json', 'rb')}
    r = requests.post(submit_url, files = answer)
    print("Status Code: " + r.status_code)

if __name__ == '__main__':
    TOKEN = get_token_input()

    data = get_data(TOKEN)

    shift, cifrado = data['numero_casas'], data['cifrado']
    data['decifrado'] = decode(cifrado, shift)

    hash_object = hashlib.sha1(data['decifrado'].encode('utf-8'))
    data['resumo_criptografico'] = hash_object.hexdigest()

    with open('answer.json', 'w') as outfile:
        json.dump(data, outfile)
    
    send_data(TOKEN)
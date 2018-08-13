import time
from bs4 import BeautifulSoup
import random
from Crypto import Random
from Crypto.PublicKey import RSA
import base64
import requests
import time
from Crypto.Cipher import AES
import base64, os
import json
import string

def fake_message():
    lines = open('sentences.txt').read().splitlines()
    myline =random.choice(lines)
    print(myline)
    return myline

def chunky(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out

def post_message_to_relay(message):

    requests.post("http://34.217.16.124:5000/blast", data={"message-ujwjejwjaq" : message})

def get_message_from_relay():

    return requests.get("http://34.217.16.124:5000/blast").text

def key_exchange_mode():

    while(1):
        time.sleep(5)
        _text = requests.get("http://34.217.16.124:5000/blast").text
        if json.loads(text)["key"] and json.loads(text)["key"] != key:
            return key

def generate_secret_key_for_AES_cipher():
    # AES key length must be either 16, 24, or 32 bytes long
    AES_key_length = 16 # use larger value in production
    # generate a random secret key with the decided key length
    # this secret key will be used to create AES cipher for encryption/decryption
    secret_key = os.urandom(AES_key_length)
    # encode this secret key for storing safely in database
    encoded_secret_key = base64.b64encode(secret_key)
    return encoded_secret_key

def encrypt_message(private_msg, encoded_secret_key, padding_character):
    # decode the encoded secret key
    secret_key = base64.b64decode(encoded_secret_key)
    # use the decoded secret key to create a AES cipher
    cipher = AES.new(secret_key)
    # pad the private_msg
    # because AES encryption requires the length of the msg to be a multiple of 16
    padded_private_msg = private_msg + (padding_character * ((16-len(private_msg)) % 16))
    # use the cipher to encrypt the padded message
    encrypted_msg = cipher.encrypt(padded_private_msg)
    # encode the encrypted msg for storing safely in the database
    encoded_encrypted_msg = base64.b64encode(encrypted_msg)
    # return encoded encrypted message
    return encoded_encrypted_msg

def decrypt_message(encoded_encrypted_msg, encoded_secret_key, padding_character):
    # decode the encoded encrypted message and encoded secret key
    secret_key = base64.b64decode(encoded_secret_key)
    encrypted_msg = base64.b64decode(encoded_encrypted_msg)
    # use the decoded secret key to create a AES cipher
    cipher = AES.new(secret_key)
    # use the cipher to decrypt the encrypted message
    decrypted_msg = cipher.decrypt(encrypted_msg)
    # unpad the encrypted message
    unpadded_private_msg = decrypted_msg.rstrip(padding_character)
    # return a decrypted original private message
    return unpadded_private_msg

def hide_in_attribute(html_page_file, shards, tag_list):

    shard_num = 0
    tag_nums = []
    for shard in shards:
        shard = shards[0]
        html_doc = open(html_page_file).read()
        soup = BeautifulSoup(html_doc, 'html.parser')
        tags = soup.find_all(tag_list[shard_num])
        num_tags = len(tags) - 1
        x = random.randint(0, num_tags)
        y = random.randint(10,100)
        tag_name = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(y)])
        tags[x][tag_name] = shard + "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        #print(soup.prettify().encode("utf-8").strip())
        fw = open(html_page_file, "w")
        #print(soup.prettify().encode("utf-8").strip())
        fw.write(soup.prettify().encode("utf-8").strip())
        tag_nums.append({x : tag_list[shard_num], "tag_name" : tag_name, "shard_num" : shard_num, "html_page_file" : html_page_file,})
        shard_num += 1
        fw.close()
        
    html_doc = open(html_page_file).read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    tags = soup.find_all(tag_list[shard_num])
    x = random.randint(0, num_tags)
    reassembly = json.dumps(tag_nums)
    tag_name = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(y)])
    tags[x][tag_name] = shard + "CCCCCCCCCCCCCCCCCCCCCCCCCCC"
    
        
    return tag_nums

def hide_metadata(html_page_file, tag_nums):
    ####
    pass

def generate_fake_data(html_page_file, tag_list):

    for i in range(10):
        html_doc = open(html_page_file).read()
        soup = BeautifulSoup(html_doc, 'html.parser')
        #note no tag or shard num passed here, letting bs do some randomization for us
        tags = soup.find_all(tag_list)
        num_tags = len(tags) - 1
        x = random.randint(0, num_tags)
        y = random.randint(10,100)
        tag_name = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(y)])        
        tags[x][tag_name] = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(y)]) + "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"
        fw = open(html_page_file, "w")
        fw.write(soup.prettify().encode("utf-8").strip())
        fw.close()

if __name__ == "__main__":

        private_msg = """
 Lorem ipsum dolor sit amet, malis recteque posidonium ea sit, te vis meliore verterem. Duis movet comprehensam eam ex, te mea possim luptatum gloriatur. Modus summo epicuri eu nec. Ex placerat complectitur eos.
"""
        padding_character = "{"

        secret_key = generate_secret_key_for_AES_cipher()
        encrypted_msg = encrypt_message(private_msg, secret_key, padding_character)
        decrypted_msg = decrypt_message(encrypted_msg, secret_key, padding_character)
        sharded_encrypted_message = chunky(encrypted_msg, 3)
        print(encrypted_msg)
        
        f = open("index.html").read()
        #print("   Secret Key: %s - (%d)" % (secret_key, len(secret_key)))
        #print("Encrypted Msg: %s - (%d)" % (encrypted_msg, len(encrypted_msg)))
        #print("Decrypted Msg: %s - (%d)" % (decrypted_msg, len(decrypted_msg)))
        #print("Sharded Msg: %s" % sharded_encrypted_message)
        #print get_message_from_relay()
        print(hide_in_attribute("index.html", sharded_encrypted_message, ["a", "div", "p"]))
        time.sleep(1)
        generate_fake_data("index.html", ["span", "div", "p"])
        time.sleep(1)
        post_message_to_relay(f)

from flask import Flask, request, send_file
from steganography.steganography import Steganography
app = Flask(__name__)

@app.route("/blast", methods = ["GET", "POST"])
def blast():
    if request.method  == "POST":
        message = request.form.get("message-ujwjejwjaq")
        print(message)
        f = open("/tmp/msg", "w")
        message = message.encode("utf-8").strip()
        f.write(message)
        f.close()

        f = open("/tmp/msg")
        return f.read()
    
    if request.method == "GET":
        f = open("/tmp/msg")
        #print(f.read())
        return f.read()

@app.route("/img/ewflwkewhnuhfnuajfjn", methods = ["GET", "POST"])
def image():

    if request.method  == "POST":
        message = request.form.get("message-ujwjejwjaq")
        print(message)
        f = open("/tmp/msg2", "w")
        message = message.encode("utf-8").strip()
        f.write(message)
        f.close()

        f = open("/tmp/msg2")
        return f.read()
    
    if request.method == "GET":
        f = open("/tmp/msg2")
        return f.read()
        
if __name__ == "__main__":


    #db = pickledb.load('keys.db', False) 

    app.run(host="0.0.0.0", debug = True)

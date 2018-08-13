from flask import Flask, request
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

#@app.route("/keys", methods = ["GET", "POST"])
#def keys():
#
#    db = pickledb.load('keys.db', False) 

if __name__ == "__main__":


    #db = pickledb.load('keys.db', False) 

    app.run(host="0.0.0.0", debug = True)

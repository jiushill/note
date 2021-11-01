from flask import Flask
from flask import request
import base64

app = Flask(__name__)

@app.route("/")
def index():
    try:
        base64data=request.args.get("name")
        print(base64data)
        if len(base64data)>0:
            print("[*] The Command Result")
            print(base64.b64decode(base64data).decode())
        return "ok"
    except Exception as error:
        pass

if __name__ == '__main__':
    app.run("0.0.0.0", 80)
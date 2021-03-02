from flask import Flask
import re

app = Flask(__name__)
alpha_num = re.compile(r'[a-z]+|[A-Z]+')

@app.route('/<name>')
def generateResponse(name=None):
    name = fix_name(name)

    if name.isupper():
        res = name.lower()
    elif name.islower():
        res = name.upper()
    else:
        res = name

    return f'Welscome, {res}, to my CSCB20 website!'

def fix_name(name):
    return ''.join(alpha_num.findall(name))

import cgi
import datetime
import wsgiref.handlers
import os
import logging
import io
import random

# logging.getLogger().setLevel(logging.DEBUG)
from flask import Flask, abort, make_response, request, send_from_directory, url_for, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
static_dir = os.path.join(os.path.dirname(__file__), 'static')

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/newgame")
def newgame():
    return render_template('newgame.html')

@app.route("/genmlist/<game>", methods=['GET'])
def genmlist_for_game(game):
    titles_fname = os.path.join(static_dir, game + ".txt")
    return _genmlist(open(titles_fname, "rb"))

@app.route("/genmlist", methods=['GET', 'POST'])
def genmlist():
    if request.method == 'GET':
        return render_template('mlistform.html')

    titles_file= request.files['titles_file']

    return _genmlist(titles_file)

def _genmlist(titles_file):
    titles = [x.strip() for x in titles_file.readlines()]

    titles.sort()
    cols = 2

    buffer = io.BytesIO()
    output = io.TextIOWrapper(buffer, encoding='utf-8', write_through=True)

    output.write('<html><body>\n')
    output.write('<table border align=center>')
    while titles:
        output.write('<tr align=left>')
        for k in range(cols):
            if titles:
                output.write('<td>[&nbsp;&nbsp]&nbsp;&nbsp;%s</td>' % titles.pop(0).decode('utf-8'))
        output.write('</tr>')
    output.write('</table><br><br>')
    output.write('</body><html>\n')

    response = buffer.getvalue()
    buffer.close()
    
    return response

@app.route("/genchits/<game>", methods=['GET'])
def genchits_for_game(game):
    titles_fname = os.path.join(static_dir, game + ".txt")
    return _genchits(open(titles_fname, "rb"))

@app.route("/genchit/<game>", methods=['GET'])
def genchit_for_game(game):
    titles_fname = os.path.join(static_dir, game + ".txt")
    return _genchits(open(titles_fname, "rb"), count=1)

@app.route("/genchits", methods=['GET', 'POST'])
def genchits():
    if request.method == 'GET':
        return render_template('chitsform.html')

    titles_file= request.files['titles_file']

    return _genchits(titles_file)

def _genchits(titles_file, count=48):
    titles = [x.strip() for x in titles_file.readlines()]

    num_chits = count
    rows = 4
    cols = 3

    buffer = io.BytesIO()
    out = io.TextIOWrapper(buffer, encoding='utf-8', write_through=True)

    out.write('<html><body>\n')
    for i in range(num_chits):
        entries = random.sample(titles, rows*cols)
        out.write('<table cellpadding=5 border align=center valign=middle>')
        for j in range(rows):
            out.write('<tr align=left>')
            for k in range(cols):
                out.write('<td>[&nbsp;&nbsp]&nbsp;&nbsp;%s</td>' % entries.pop().decode('utf-8'))
            out.write('</tr>')
        out.write('</table><br><br>')
    out.write('</body><html>\n')

    response = buffer.getvalue()
    buffer.close()
    
    return response

if __name__ == '__main__':
    main()


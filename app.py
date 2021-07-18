from flask import Flask, request, render_template, session, redirect
from flask.helpers import url_for
import pandas as pd


app = Flask(__name__)


@app.route('/', methods=("POST", "GET"))
def index():
    return render_template('index.html')


@app.route('/calc', methods=['POST'])
def calculate():
    try:
        x1 = int(request.form['x1'])
        y1 = int(request.form['y1'])
        x2 = int(request.form['x2'])
        y2 = int(request.form['y2'])
        return html_table(x1, y1, x2, y2)
    except:
        return "<h1>!!!input Integer number Only!!!!</h1>"


def html_table(x1, y1, x2, y2):

    origZone = FindZone(x1, y1, x2, y2)

    data = {
        'Zone 0': [],
        'D': [],
        'NE/E': []
    }
    data['*Zone '+str(origZone)] = []

    X1, Y1 = ConvertToZone0(x1, y1, origZone)
    X2, Y2 = ConvertToZone0(x2, y2, origZone)

    MidPoint(X1, Y1, X2, Y2, origZone, data)
    print(data.keys())
    df = pd.DataFrame(data)
    df = df.head(20)
    return render_template('simple.html',  tables=[df.to_html(classes='table', header="true")])
    # return render_template('simple.html',  tables=[df.to_html(classes='table table-striped')], titles=df.columns.values)


def ConvertToZone0(X, Y, zone):
    if zone == 1:
        x = Y
        y = X
    elif zone == 2:
        x = Y
        y = -X
    elif zone == 3:
        x = -X
        y = Y
    elif zone == 4:
        x = -X
        y = -Y
    elif zone == 5:
        x = -Y
        y = -X
    elif zone == 6:
        x = -Y
        y = X
    elif zone == 7:
        x = X
        y = -Y
    else:
        x = X
        y = Y
    return (x, y)


def FindZone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    if abs(dx) > abs(dy):
        if dx > 0 and dy > 0:
            zone = 0
        elif dx < 0 and dy > 0:
            zone = 3
        elif dx < 0 and dy < 0:
            zone = 4
        elif dx > 0 and dy < 0:
            zone = 7
    else:
        if dx > 0 and dy > 0:
            zone = 1
        elif dx < 0 and dy > 0:
            zone = 2
        elif dx < 0 and dy < 0:
            zone = 5
        elif dx > 0 and dy < 0:
            zone = 6

    return zone


def MidPoint(x1, y1, x2, y2, origZone, data):
    dx = x2-x1
    dy = y2-y1
    D = 2*dy-dx
    delNE = 2*(dy-dx)
    delE = 2*dy
    print('delNE: '+str(delNE))
    print('delE: '+str(delE))
    x = x1
    y = y1
    if D > 0:
        NE = 'NE'
    else:
        NE = 'E'
    Draw(x, y, D, origZone, NE, data)
    while(x <= x2):
        x += 1
        if D > 0:
            y += 1
            D = D+delNE
            if(D > 0):
                NE = 'NE'
            else:
                NE = 'E'
        else:
            D = D + delE
            if(D > 0):
                NE = 'NE'
            else:
                NE = 'E'

        Draw(x, y, D, origZone, NE, data)


def Draw(x, y, D, origZone, NE, data):
    data['Zone 0'].append((x, y))
    data['D'].append(D)
    data['NE/E'].append(NE)
    data['*Zone '+str(origZone)].append(OriginalZone(x, y, origZone))


def OriginalZone(X, Y, zone):
    if zone == 1:
        x = Y
        y = X
    elif zone == 2:
        x = -Y
        y = X
    elif zone == 3:
        x = -X
        y = Y
    elif zone == 4:
        x = -X
        y = -Y
    elif zone == 5:
        x = -Y
        y = -X
    elif zone == 6:
        x = Y
        y = -X
    elif zone == 7:
        x = X
        y = -Y
    else:
        x = X
        y = Y
    return (x, y)


if __name__ == '__main__':
    app.run(port=4000)

from flask import Flask, jsonify, render_template, request
import json
import time

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

JSON = {}

def set_data():
    global JSON
    with open('static/default_figure.js', encoding="utf8") as dataFile:
        data = dataFile.read()
        obj = data[data.find('{') : data.rfind('}')+1]
        jsonObj = json.loads(obj)
        dataFile.close()

    JSON = jsonObj


def show_searched_movie_plot(movie_title):
    near = 1
    far = 40
    newx, newy, newz, newtext = [], [], [], []
    new_fullx, new_fully, new_fullz, new_fulltext = [], [], [], []
    local_json = JSON

    search = movie_title
    if not search:
        # with open('static/figure.js', 'w') as f:
        #     full = 'var figure = ' + str(local_json)
        #     f.write(full)
        #     f.close()
        #     is_success = 0

        return local_json['data']

    
    data_0 = local_json['data'][0]
    data_1 = local_json['data'][1]

    FULLX, FULLY, FULLZ, FULLTEXT = data_0['x'], data_0['y'], data_0['z'], data_0['text']
    # EMPYTX, EMPYTY, EMPYTZ, EMPYTTEXT, = EMPTY_DATA['x'], EMPTY_DATA['y'], EMPTY_DATA['z'], EMPTY_DATA['text']

    pos = FULLTEXT.index(search)
    val_x, val_y, val_z = FULLX[pos], FULLY[pos], FULLZ[pos]

    print('postion of ' + search + ':' + str(val_x) + " " + str(val_y) + " " + str(val_z) )
    
    for i in range(len(FULLX)):
        if FULLX[i]>=(val_x-near) and FULLX[i]<=(val_x+near) and FULLY[i]>=(val_y-near) and FULLY[i]<=(val_y+near) and FULLZ[i]>=(val_z-near) and FULLZ[i]<=(val_z+near):
            #print(str(FULLX[i]) + " " + str(FULLY[i]) + " " + str(FULLZ[i]) )
            #print(FULLTEXT[i])
            newx.append(FULLX[i])
            newy.append(FULLY[i])
            newz.append(FULLZ[i])
            #pos_list.append(i)
            newtext.append(FULLTEXT[i])
        elif FULLX[i]>=(val_x-far) and FULLX[i]<=(val_x+far) and FULLY[i]>=(val_y-far) and FULLY[i]<=(val_y+far) and FULLZ[i]>=(val_z-far) and FULLZ[i]<=(val_z+far):
            new_fullx.append(FULLX[i])
            new_fully.append(FULLY[i])
            new_fullz.append(FULLZ[i])
            #pos_list.append(i)
            new_fulltext.append(FULLTEXT[i])

    data_0['x'] = new_fullx
    data_0['y'] = new_fully
    data_0['z'] = new_fullz
    data_0['text'] = new_fulltext
    local_json['data'][0] = data_0

    data_1['x'] = newx
    data_1['y'] = newy
    data_1['z'] = newz
    data_1['text'] = newtext
    local_json['data'][1] = data_1

    
    # is_success = -1
    # local_json = json.dumps(local_json, indent=4)

    #print(local_json)

    # with open('static/figure.js', 'w') as f:
    #     full = 'var figure = ' + str(local_json)
    #     f.write(full)
    #     f.close()
    #     is_success = 0

    # return is_success
    return local_json['data']


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET','POST'])
def search():
    movie_title = request.form['myMovie']
    print('\n\n'+str(movie_title)+'\n')
    # movie_title = 'Babe'

    big_data, small_data = show_searched_movie_plot(movie_title)

    x1, y1, z1, text1 = small_data['x'], small_data['y'], small_data['z'], small_data['text']
    x2, y2, z2, text2 = big_data['x'], big_data['y'], big_data['z'], big_data['text']

    print('len of sugesstions: ' + str(len(x1)))
    print('len of total is: ' + str(len(x2) + len(x1)))

    return jsonify(x1=x1, y1=y1, z1=z1, text1=text1, x2=x2, y2=y2, z2=z2, text2=text2)


if __name__ == '__main__':
    set_data()
    app.run(debug = True)

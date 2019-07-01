from flask import Flask, request, render_template
import json
import time

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

newx, newy, newz, newtext = [], [], [], []
new_fullx, new_fully, new_fullz, new_fulltext = [], [], [], []
	
@app.route('/search', methods=['POST','GET'])
def search():
	movie_title = ''
	if request.method == 'POST':
		movie_title = request.form['myMovie']
		is_success = show_searched_movie_plot(movie_title)
		print(is_success)
		print(request.form['myMovie'])
		#time.sleep(0)
	#reload_js = 1
	x1, y1, z1, text1 = [], [], [], []
	x2, y2, z2, text2 = [], [], [], []
	x1 = newx
	y1 = newx
	z1 = newz
	text1 = newtext
	x2 = new_fullx
	y2 = new_fully
	z2 = new_fullz
	print('len of sugesstions: ' + str(len(x1)))
	print('len of total is: ' + str(len(x2) + len(x1)))
	text2 = new_fulltext
	return render_template("index.html", movie_title=movie_title, x1=x1, y1=y1, z1=z1, text1=text1, x2=x2, y2=y2, z2=z2, text2=text2)


def show_searched_movie_plot(movie_title):

	with open('static/default_figure.js', encoding="utf8") as dataFile:
	    data = dataFile.read()
	    obj = data[data.find('{') : data.rfind('}')+1]
	    jsonObj = json.loads(obj)
	    dataFile.close()
	    

	near = 1
	far = 40

	search = movie_title
	if search=='':
		with open('static/figure.js', 'w') as f:
			full = 'var figure = ' + str(jsonObj)
			f.write(full)
			f.close()
			is_success = 0

		return is_success


	data_ob_0 = jsonObj['data'][0]
	data_ob_1 = jsonObj['data'][1]
	listx = data_ob_0['x']
	listy = data_ob_0['y']
	listz = data_ob_0['z']
	listtext = data_ob_0['text']

	pos = listtext.index(search)
	val_x = listx[pos]
	val_y = listy[pos]
	val_z = listz[pos]
	print('postion of ' + search + ':' + str(val_x) + " " + str(val_y) + " " + str(val_z) )
	newx.clear()
	newy.clear()
	newz.clear()
	newtext.clear()
	new_fullx.clear()
	new_fully.clear()
	new_fullz.clear()
	new_fulltext.clear()
    
	for i in range(len(listx)):
		if listx[i]>=(val_x-near) and listx[i]<=(val_x+near) and listy[i]>=(val_y-near) and listy[i]<=(val_y+near) and listz[i]>=(val_z-near) and listz[i]<=(val_z+near):
			#print(str(listx[i]) + " " + str(listy[i]) + " " + str(listz[i]) )
			#print(listtext[i])
			newx.append(listx[i])
			newy.append(listy[i])
			newz.append(listz[i])
			#pos_list.append(i)
			newtext.append(listtext[i])
		elif listx[i]>=(val_x-far) and listx[i]<=(val_x+far) and listy[i]>=(val_y-far) and listy[i]<=(val_y+far) and listz[i]>=(val_z-far) and listz[i]<=(val_z+far):
			new_fullx.append(listx[i])
			new_fully.append(listy[i])
			new_fullz.append(listz[i])
			#pos_list.append(i)
			new_fulltext.append(listtext[i])


	data_ob_1['x'] = newx
	data_ob_1['y'] = newy
	data_ob_1['z'] = newz
	data_ob_1['text'] = newtext
	jsonObj['data'][1] = data_ob_1

	data_ob_0['x'] = new_fullx
	data_ob_0['y'] = new_fully
	data_ob_0['z'] = new_fullz
	data_ob_0['text'] = new_fulltext
	jsonObj['data'][0] = data_ob_0
	is_success = -1
	jsonObj = json.dumps(jsonObj, indent=4)

	#print(jsonObj)

	with open('static/figure.js', 'w') as f:
		full = 'var figure = ' + str(jsonObj)
		f.write(full)
		f.close()
		is_success = 0

	return is_success



if __name__ == '__main__':
   app.run(debug = True)

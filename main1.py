import json

newx, newy, newz, newtext = [], [], [], []
new_fullx, new_fully, new_fullz, new_fulltext = [], [], [], []

def show_searched_movie_plot(movie_title):

	with open('static/default_figure.js', encoding="utf8") as dataFile:
	    data = dataFile.read()
	    obj = data[data.find('{') : data.rfind('}')+1]
	    jsonObj = json.loads(obj)
	    dataFile.close()
	    

	near = 1
	far = 40

	search = movie_title
	#print('yes i am being called -- ' + search )
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

	#print(newx)
	#print(newy)
	#print(newz)


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


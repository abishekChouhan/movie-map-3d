from flask import Flask, request, render_template
import main1
import time

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0



@app.route('/')
def index():
	return render_template('index.html')
	
@app.route('/search', methods=['POST','GET'])
def search():
	movie_title = ''
	if request.method == 'POST':
		movie_title = request.form['myMovie']
		is_success = main1.show_searched_movie_plot(movie_title)
		print(is_success)
		print(request.form['myMovie'])
		#time.sleep(0)
	#reload_js = 1
	x1, y1, z1, text1 = [], [], [], []
	x2, y2, z2, text2 = [], [], [], []
	x1 = main1.newx
	y1 = main1.newx
	z1 = main1.newz
	text1 = main1.newtext
	x2 = main1.new_fullx
	y2 = main1.new_fully
	z2 = main1.new_fullz
	print('len of sugesstions: ' + str(len(x1)))
	print('len of total is: ' + str(len(x2) + len(x1)))
	text2 = main1.new_fulltext
	return render_template("index1.html", movie_title=movie_title, x1=x1, y1=y1, z1=z1, text1=text1, x2=x2, y2=y2, z2=z2, text2=text2)
	


if __name__ == '__main__':
   app.run(debug = True)

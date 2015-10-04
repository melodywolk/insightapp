from flask import render_template, request
from app import app
import pymysql as mdb
import pandas as pd
import folium
import matplotlib.pyplot as plt
from colormap import rgb2hex
import random
import numpy as np
import os

path_to_wikipaintings = path_to_wikipaintings
path_to_validation = path_to_validation

db = mdb.connect(user="root", host="localhost", passwd="password", db="testdb", charset='utf8')
list_style=['Detailed','Pastel','Melancholy','Noir','HDR','Vintage','Long Exposure','Horror','Sunny','Bright','Hazy','Bokeh','Serene','Texture','Ethereal', 'Macro','Depth of Field', 'Geometric Composition', 'Minimal','Romantic']

@app.route('/')
@app.route('/index')
def index():
	return render_template("cover.html", title='Home')

@app.route('/about')
def about():
	return render_template("about.html", title='About')

@app.route('/slider')
def slider():
	string = request.args.get('style1')
	style1 = list_style.index(string)
	print style1
  	with db:
    		cur = db.cursor()
		cur.execute("SELECT lat,lon,url,user, style1,sval1 FROM New_Flickr_info WHERE style1='%s' AND sval1>.7;" % style1)
    		query_results = cur.fetchall()
  	pic = []
	user = []
	pic_id = []
	sval = []
  	for result in query_results:
    		pic.append(result[2])
		user.append(result[3])
		pic_id.append(result[2][7:-4])
		sval.append(round(float(result[5]),2))

	combined = zip(pic, user, pic_id, sval)
	random.shuffle(combined)
	pic[:], user[:], pic_id[:], sval[:] = zip(*combined)
	
	return render_template("carousel.html", title='Test', pic = pic, user=user, pic_id=pic_id, sval=sval)


@app.route('/user', methods=['POST', 'GET'])
def user():
	user = request.args.get('user', '')
	pic_id = request.args.get('pic_id', '')
	start = 'http://'
	end = '.jpg'
	char = start+pic_id+end
	with db:
    		cur = db.cursor()
		cur.execute("SELECT lat,lon,url,user, style, name, profile FROM user_info WHERE user='%s' AND url='%s';" % (user, char))
    		query_results = cur.fetchall()
        for result in query_results:
		lat=result[0]
		lon=result[1]
		url=result[2]
		user=result[3]
                style = list_style[result[4]]
		name = result[5]
		profile = result[6]

	return render_template("output2.html", lat=lat, lon=lon, url=url, name=name, profile=profile, style=style)

@app.route('/output')
def output():
  	string = request.args.get('style1')
	style1 = list_style.index(string)
	print style1
        tileset = r'http://stamen-tiles-{s}.a.ssl.fastly.net/watercolor/{z}/{x}/{y}.png'
        attribution = 'Map data by OpenStreetMap, under ODbL.'
        map = folium.Map(location=[37.426327,-122.141076],zoom_start=2, tiles=tileset, 
                     attr=attribution)
  	with db:
    		cur = db.cursor()
		cur.execute("SELECT lat,lon,url,user, style1,sval1 FROM New_Flickr_info WHERE style1='%s' AND sval1>.7;" % style1)
    		query_results = cur.fetchall()

  	lat = []
	lon = []
	url = []
	user = []
	s= []
        for result in query_results:
		lat.append(result[0])
		lon.append(result[1])
		url.append(result[2])
		user.append(result[3])
		s.append(result[4])

	mydata = pd.DataFrame(lat, columns=['lat'])
	mydata['lon'] = lon
	mydata['url'] = url
	mydata['user'] = user
	mydata['style1']=s

	for _, df in mydata.iterrows():
		color = rgb2hex(*plt.cm.Spectral(df['style1']/20))
		map.circle_marker(
			location=[df['lat'], df['lon']],
			popup='<img src={url} width=200 height=200> <br> {style}'.format(url=df['url'], style=list_style[df['style1']]),
			fill_color=color,
			line_color=color,
			radius=40,
			)
	map.create_map(path='/Users/wolk/Desktop/Insight/Myapp/app/templates/osm.html')
	return render_template('osm.html')

@app.route('/minimalism')
def graph_mini(chartID = 'chart_ID', chart_type = 'bar', chart_height = 500):
 
	data = pd.read_csv(path_to_wikipaintings+'wikipaintings_oct2013.csv')
	images = data['image_url'][data['style']=='Minimalism']
	name = data['artist_slug'][data['style']=='Minimalism']
	date = data['date'][data['style']=='Minimalism']
	
        combined = zip(images, name, date)
	random.shuffle(combined)
	images[:], name[:], date[:] = zip(*combined)
	
        df = pd.read_csv(path_to_validation+'minimalism.csv')
       
        new=pd.DataFrame(df['style1'])
	new['sval1']=df['sval1']

	test = new.groupby(('style1'))
	mycount = test.count()

	chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
	series = [{"name": 'Labels', "data":list(np.array(mycount['sval1'])) }]
	title = {"text": 'Labels'} 
	xAxis = {"categories":list_style}
	yAxis = {"title": {"text": 'Counts'}}
	return render_template('minimalism.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis, pic=list(images), name=list(name), date=list(date) )


@app.route('/abstract')
def graph_abs(chartID = 'chart_ID', chart_type = 'bar', chart_height = 500):
 
	data = pd.read_csv(path_to_wikipaintings+'wikipaintings_oct2013.csv')
	images = data['image_url'][data['style']=='Abstract Art']
	name = data['artist_slug'][data['style']=='Abstract Art']
	date = data['date'][data['style']=='Abstract Art']	

        combined = zip(images, name, date)
	random.shuffle(combined)
	images[:], name[:], date[:] = zip(*combined)
	
        df = pd.read_csv(path_to_validation+'abstract.csv')
       
        new=pd.DataFrame(df['style1'])
	new['sval1']=df['sval1']

	test = new.groupby(('style1'))
	mycount = test.count()

	chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
	series = [{"name": 'Labels', "data":list(np.array(mycount['sval1'])) }]
	title = {"text": 'Labels'} 
	xAxis = {"categories":list_style}
	yAxis = {"title": {"text": 'Counts'}}
	return render_template('abstract.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis, pic=list(images), name=list(name), date=list(date) )
	
@app.route('/photorealism')
def graph_real(chartID = 'chart_ID', chart_type = 'bar', chart_height = 500):
         
        data = pd.read_csv(path_to_validation+'pictures.csv')
	print data.columns
	images = data['url']
	name = data['author']
	date = data['date']	

        combined = zip(images, name, date)
	random.shuffle(combined)
	images[:], name[:], date[:] = zip(*combined)	

        df = pd.read_csv(path_to_validation+'photorealism.csv')
       
        new=pd.DataFrame(df['style1'])
	new['sval1']=df['sval1']

	test = new.groupby(('style1'))
	mycount = test.count()

	chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
	series = [{"name": 'Labels', "data":list(np.array(mycount['sval1'])) }]
	title = {"text": 'Labels'} 
	xAxis = {"categories":list_style}
	yAxis = {"title": {"text": 'Counts'}}
	return render_template('photorealism.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis, pic=list(images), name=list(name), date=list(date) )


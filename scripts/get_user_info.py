import matplotlib.pyplot as plt
import flickrapi
import pandas as pd
import pymysql as mdb

api_key = '...'
api_secret = '...'

flickr = flickrapi.FlickrAPI(api_key,secret=api_secret,format='parsed-json')

db = mdb.connect(user="root", host="localhost", passwd="password", db="testdb", charset='utf8')

with db:
  cur = db.cursor()
  cur.execute("SELECT lat,lon,url,user, style1 FROM new_flickr_info;")
  query_results = cur.fetchall()


users = []
lat = []
lon = []
url = []
style = []

for result in query_results:
    lat.append(result[0])
    lon.append(result[1])
    url.append(result[2])
    users.append(result[3])
    style.append(result[4])

name = []
profile = []                
for user in users:
    r = flickr.people.getInfo(user_id=user)
    if "person" not in r:
      print "Unknown"
      name.append("Unknown")
      profile.append("https://www.flickr.com/")
    else:
      print r['person']['profileurl']['_content']
      name.append(r['person']['username']['_content'])
      profile.append(r['person']['profileurl']['_content'])

data_user = pd.DataFrame(lat, columns=['lat'])
data_user['lon'] = lon
data_user['url'] = url
data_user['user'] = users
data_user['style'] = style
data_user['name'] = name
data_user['profile'] = profile

data_user.to_csv('user_info.csv', encoding='utf-8')


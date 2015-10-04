import flickrapi
import pandas as pd
from PIL import Image
from StringIO import StringIO
import urllib2
import datetime 
from time import time, mktime
import caffe
import numpy as np
import pymysql as mdb


path_to_caffe='...' #path to caffe

model_file = path_to_caffe + 'models/finetune_flickr_style/deploy.prototxt'
pretrained = path_to_caffe + 'models/finetune_flickr_style/finetune_flickr_style.caffemodel'
mean_file = path_to_caffe + 'python/caffe/imagenet/ilsvrc_2012_mean.npy'


net = caffe.Classifier(model_file, pretrained,
                       mean=np.load(mean_file).mean(1).mean(1),
                       channel_swap=(2,1,0),
                       raw_scale=255,
                       image_dims=(256, 256))

api_key = '...' #your secret key
api_secret = '...' 

flickr = flickrapi.FlickrAPI(api_key,secret=api_secret,format='parsed-json')

# Select all pictures taken between start date and end date
start = datetime.datetime(2015, 8, 1, 0, 0)
end = datetime.datetime(2015, 9, 1, 0, 0)

start_stamp = int(mktime(start.timetuple()))
end_stamp = int(mktime(end.timetuple()))
r = flickr.photos_search(text=['painting'], tag_mode = 'all', sort = 'relevance', safe_search=1, per_page=500, min_taken_date=start_stamp, max_taken_date=end_stamp, page=2)

i=0

path_to_image = '...' #your path to store the images

lat=[]
lon=[]
url=[]
user=[]
style1=[]
style2=[]
style3=[]
style4=[]
style5=[]
sval1=[]
sval2=[]
sval3=[]
sval4=[]
sval5=[]

for p in r['photos']['photo']:
    location = flickr.photos.geo.getLocation(photo_id = p['id'])
    if location['stat']=='ok':
        url_pic='http://farm'+str(p['farm'])+'.staticflickr.com/'+str(p['server'])+'/'+str(p['id'])+'_'+str(p['secret'])+'.jpg'
        url.append(url_pic)
        lat.append(location['photo']['location']['latitude'])
        lon.append(location['photo']['location']['longitude'])
        user.append(p['owner'])
        img = Image.open(StringIO(urllib2.urlopen(url_pic).read()))
        img.save(path_to_image+'img'+str(i)+'.jpg')
        input_image = caffe.io.load_image(path_to_image+'img'+str(i)+'.jpg')
        prediction = net.predict([input_image])[0]
        classif_array_top5 = prediction.argsort()[-5:][::-1]
        classif_array = prediction[classif_array_top5]
        style1.append(classif_array_top5[0]),
        sval1.append(classif_array[0])
        style2.append(classif_array_top5[1]),
        sval2.append(classif_array[1])
        style3.append(classif_array_top5[2]),
        sval3.append(classif_array[2])
        style4.append(classif_array_top5[3]),
        sval4.append(classif_array[3])
        style5.append(classif_array_top5[4]),
        sval5.append(classif_array[4])
        i+=1

mydata = pd.DataFrame(lat, columns=['lat'])
mydata['lon'] = lon
mydata['url'] = url
mydata['user'] = user
mydata['style1']=style1
mydata['style2']=style2
mydata['style3']=style3
mydata['style4']=style4
mydata['style5']=style5
mydata['sval1']=sval1
mydata['sval2']=sval2
mydata['sval3']=sval3
mydata['sval4']=sval4
mydata['sval5']=sval5

con = mdb.connect('localhost', 'root', 'password', 'testdb')
mydata.to_sql(con=con, name='your_table', if_exists='append', flavor='mysql')



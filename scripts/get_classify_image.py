import pandas as pd
import re
from PIL import Image
from StringIO import StringIO
import urllib2


PATH_TO_DATASET = '...'
df = pd.read_csv(PATH_TO_DATASET+'toclassify.csv')

path_to_image = '...' #path to your images

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

i=0
for link in df['url']:
    img = Image.open(StringIO(urllib2.urlopen(link).read()))
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

mydata = pd.DataFrame(df['lat'], columns=['lat'])
mydata['lon'] = df['lon']
mydata['url'] = df['url']
mydata['user'] = df['user']
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

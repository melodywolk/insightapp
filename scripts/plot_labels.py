import pandas as pd
import pymysql as mdb
import numpy as np
import matplotlib.pyplot as plt


x = np.array([0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5,13.5,14.5,15.5,16.5,17.5,18.5,19.5])
style=['Detailed','Pastel','Melancholy','Noir','HDR','Vintage','Long Exposure','Horror','Sunny','Bright','Hazy','Bokeh','Serene','Texture','Ethereal', 'Macro','Depth of Field', 'Geo Composition', 'Minimal','Romantic']


db = mdb.connect(user="root", host="localhost", passwd="password", db="testdb", charset='utf8')
with db:
    cur = db.cursor()
    cur.execute("SELECT lat,lon,url,user, style1,sval1 FROM New_Flickr_info;")
    query_results = cur.fetchall()
style1 = []
sval1 = []
for result in query_results:
 style1.append(result[4])
 sval1.append(result[5])
new = pd.DataFrame(style1)
new['sval1']=sval1
new.columns = ['style1', 'sval1']

test = new.groupby(('style1'))
mymean = test.agg(np.mean)
myvar = test.agg(np.var)


fig = plt.figure(figsize=(5,5),dpi=300,facecolor='black')
ax = fig.add_subplot(1,1,1,axisbg='k')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_linewidth(0.5)
ax.spines['left'].set_linewidth(0.5)
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')

ax.title.set_color('white')
ax.yaxis.label.set_color('white')
ax.xaxis.label.set_color('white')
ax.tick_params(axis='x', colors='white', labelsize=12)
ax.tick_params(axis='y', colors='white', labelsize=15)

ax.tick_params(axis='both', direction='in')
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()

ax.set_title('Model confidence')
plt.plot(x-0.5, mymean['sval1'], 'w', lw=2)
plt.ylabel("Mean first label probability")
plt.ylim(ymax = 1, ymin = 0)
plt.xticks(x, style, rotation='vertical')
plt.fill_between(x-0.5,  mymean['sval1'] - np.sqrt(myvar['sval1']), mymean['sval1'] + np.sqrt(myvar['sval1']), edgecolor='#0d3954', color='#45a4af', alpha=0.4)
plt.savefig("accuracy.png",\
  bbox_inches='tight',\
  facecolor=fig.get_facecolor(),\
  transparent=True)

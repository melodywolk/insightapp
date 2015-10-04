import pandas as pd
import pymysql as mdb
import numpy as np
import matplotlib.pyplot as plt

x = np.array([0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5,13.5,14.5,15.5,16.5,17.5,18.5,19.5])
style=['Detailed','Pastel','Melancholy','Noir','HDR','Vintage','Long Exposure','Horror','Sunny','Bright','Hazy','Bokeh','Serene','Texture','Ethereal', 'Macro','Depth of Field', 'Geo Composition', 'Minimal','Romantic']


df = pd.read_csv('/Users/wolk/Desktop/Insight/scripts/Validation/post_imp.csv')

new=pd.DataFrame(df['style1'])
new['sval1']=df['sval1']

test = new.groupby(('style1'))
mycount = test.count()


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

ax.set_title('6000 Impressionism paintings')
count = np.array(mycount['sval1'])
myframe = pd.DataFrame(count, columns=['count'])
myframe['x'] = x-0.5

new = myframe.sort('count', ascending=True)
print new
new_style = []
for i in new['x']:
    new_style.append(style[int(i)])

print  new_style

plt.barh(x[10:]-0.5, new['count'][10:], color='#45a4af', edgecolor='#0d3954', linewidth=2)
plt.yticks(x[10:], new_style[10:])
plt.subplots_adjust(left=0.25, bottom=0.1, top=0.9, right=0.9)

plt.savefig("dark.png",\
  bbox_inches='tight',\
  facecolor=fig.get_facecolor(),\
  transparent=True)

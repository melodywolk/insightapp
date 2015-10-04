import pandas as pd
import re

#path for Flickr 100M csv data file
PATH_TO_DATASET = '...'

name_list = ['Photo/video identifier','NSID','nickname','Date_taken','Date_uploaded','device','Title',\
             'Description','user_tags','machine_tags','Longitude','Latitude','Accuracy','page_URL','download_URL',\
             'License_name','License URL','server_ID','farm_ID','secret','secret_orig','extension','pv_marker']

nrows = nrows #in case of memory issues              

photo = pd.read_csv(PATH_TO_DATASET, nrows=nrows, sep='\t',header=None,names =name_list)

#Select only pictures and not videos
pnew = photo[['Latitude','Longitude', 'download_URL','NSID', 'nickname', 'user_tags']][photo['pv_marker']==0]


#Select where tags exist
pnew = pnew[['Latitude','Longitude', 'download_URL','NSID', 'nickname', 'user_tags']][pnew['user_tags'].notnull()==True]

#Select where tags contain 'painting'
pnew = pnew[pnew['user_tags'].str.contains('painting', re.IGNORECASE)]

#Select where geo coordinates
pnew = pnew[['Latitude','Longitude', 'download_URL','NSID']][pnew['Latitude'].notnull()]

pnew.columns = ['lat', 'lon', 'url', 'user']
pnew.to_csv('toclassify.csv')


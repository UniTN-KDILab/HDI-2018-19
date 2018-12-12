import os 
import pandas as pd 
import googlemaps

# Autentcation with an API key 

gmaps = googlemaps.Client(key='AIzaSyDS2k7BAZh6enNKobgBIYeDM3kUlPWXaLM')

# change of the dirctory and list of the present directories, equal to the names of the heath care facility

PATH='./strutture_ospedaliere'
os.chdir(PATH)
l=os.listdir()

# search of the coordinates in latitude and longitude of the health care facility and constitution of a Series, that will saved in a csv file

diz={}
for i in l:
        print(i)
        g=gmaps.geocode(i)
        if len(g)!=0:
                t=(g[0]['geometry']['location']['lat'],g[0]['geometry']['location']['lng'])
                diz[i]=t
        else:
                diz[i]=('NaN')
        

latlng=pd.Series(diz)

latlng.to_csv('../Hospital_latlng.csv')

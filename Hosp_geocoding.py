import os 
import pandas as pd 
import googlemaps
import difflib



# Autentcation with an API key 

gmaps = googlemaps.Client(key='AIzaSyDS2k7BAZh6enNKobgBIYeDM3kUlPWXaLM')

# change of the dirctory and list of the present directories, equal to the names of the heath care facility

PATH='./strutture_ospedaliere'
os.chdir(PATH)
l=os.listdir()
l.sort()

# search of the coordinates in latitude and longitude of the health care 

Hosp_address=pd.read_excel('../Ospedali.xls',header=1)

#Convert some acronyms

sigle={'A.O.':'Azienda Ospedaliera','A.O.SSN':'Azienda ospedaliera integrata','A.O.U.U.':'Azienda ospedaliera universitaria',
                       'CCA':'Casa di Cura','CC':'Casa di Cura','E.R.':'Ente di Ricerca',
                        'IRCCSf':'Istituto di Ricovero','IRCCSpr':'Istituto di Ricovero Privato',
                        'IRCCSpub':'Istituto di Ricovero','Osp.':'Ospedale','Osp.C.':'Ospedale',
                        'Pol.U.':'Policlinico Universitario','Pres.':'Presidio'}

#find the cordinate using the address, after the name of the structure was identified in xls file, and costruction of the dictionary to build the dataframe

diz={}
diz_lat={}
diz_lng={}
lista=[]

for i in l:
        fil=Hosp_address[['Denominazione struttura', 'Comune', 'Sigla provincia' , 'Indirizzo']][Hosp_address['Comune']==i.split("-")[-1].split('(')[0].lstrip(" ").rstrip('\xa0').upper()]
        
        if i.split(" ")[0] in sigle.keys():          
                s=i.replace(i.split(" ")[0],sigle[i.split(" ")[0]])
        if s.find('S.itario')!=-1 :
                s=s.replace('S.itario','Sanintario')

        if s.find('S.atrix')!=-1 :
                s=s.replace('S.atrix','Sanatrix')


        # if the city of the hospital is not present, we use try to obtain directily the location with the name, not the address

        if fil.shape[0]==0:
                g=gmaps.geocode(s)
                if len(g)==0:
                        we='{}, {} ({})'.format(fil['Denominazione struttura'].values[0], fil['Comune'].values[0], fil['Sigla provincia'].values[0])
                        g=gmaps.geocode(we)
                t=(float(g[0]['geometry']['location']['lat']),float(g[0]['geometry']['location']['lng']))
                print(t)
                diz[i]=t
                diz_lat[i]=float(t[0])
                diz_lng[i]=float(t[1]) 
        # if there's only one structure for the city, we use directly the given address to obtain the location
        elif fil.shape[0]==1:
                we='{}, {} ({})'.format(fil["Indirizzo"].values[0], fil['Comune'].values[0], fil['Sigla provincia'].values[0])
                g=gmaps.geocode(we)
                if len(g)==0:
                        we='{}, {} ({})'.format(fil['Denominazione struttura'].values[0], fil['Comune'].values[0], fil['Sigla provincia'].values[0])
                        g=gmaps.geocode(we)
                t=(float(g[0]['geometry']['location']['lat']),float(g[0]['geometry']['location']['lng']))
                print(t)
                diz[i]=t
                diz_lat[i]=float(t[0])
                diz_lng[i]=float(t[1]) 
        # if there are more structure for that city, we try to find the best match for the name of the structure, to use its address and obtain the location
        else:
                match=difflib.get_close_matches(s.upper(),fil['Denominazione struttura'].values,cutoff=0.3)
                match=list(set(match))
                
                for cutoff in [0.4,0.5,0.6,0.7,0.8,0.9,0.95,0.97,1.0]:
                        m=difflib.get_close_matches('-'.join(s.split('-')[:-1]).upper(),match,cutoff=cutoff)
                        if len(m)==0:
                                break
                        match=m
                        if len(match)==1:
                                break  
                match=list(set(match))
                if len(match)==0:
                        match=difflib.get_close_matches(s.upper(),fil['Denominazione struttura'].values,cutoff=0.2)
                
                if len(match)==0:
               
                        for cutoff in [0.4,0.5,0.6,0.7,0.8,0.9,0.95,0.97,1.0]:
                                m=difflib.get_close_matches(s,fil['Denominazione struttura'].values,cutoff=cutoff)
                                if len(m)==0:
                                        break
                                match=m
                                if len(match)==1:
                                        break
                
                match=list(set(match))
                if len(match)==0:
                        g=gmaps.geocode(s)
                        if len(g)==0:
                                we='{}, {} ({})'.format(fil['Denominazione struttura'].values[0], fil['Comune'].values[0], fil['Sigla provincia'].values[0])
                                g=gmaps.geocode(we)
                        t=(float(g[0]['geometry']['location']['lat']),float(g[0]['geometry']['location']['lng']))
                        print(t)
                        diz[i]=t
                        diz_lat[i]=float(t[0])
                        diz_lng[i]=float(t[1]) 
                else:
                        nome_struttura=match[0]

                        fil=fil[fil['Denominazione struttura']==nome_struttura]

                        we='{}, {} ({})'.format(fil["Indirizzo"].values[0], fil['Comune'].values[0], fil['Sigla provincia'].values[0])
                        g=gmaps.geocode(we)
                        if len(g)==0:
                                we='{}, {} ({})'.format(fil['Denominazione struttura'].values[0], fil['Comune'].values[0], fil['Sigla provincia'].values[0])
                                g=gmaps.geocode(we)
                        t=(float(g[0]['geometry']['location']['lat']),float(g[0]['geometry']['location']['lng']))
                        print(t)
                        diz[i]=t
                        diz_lat[i]=float(t[0])
                        diz_lng[i]=float(t[1]) 


# building and writing the dataframe

location=pd.Series(diz)
lat=pd.Series(diz_lat)
lng=pd.Series(diz_lng)

diz_df={'location':location, 'latitude':lat, 'longitude': lng}

df=pd.DataFrame(diz_df)

df.to_csv('../Hospital_latlng.csv')
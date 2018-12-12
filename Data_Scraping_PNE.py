import requests
import json
import re
from bs4 import BeautifulSoup
import pandas as pd
import os





def request_hosp(url_hosp):
    r= requests.get(url_hosp)
    data = json.loads(r.text)

    nodes=data["nodes"]

    # I find the index to divide the nodes list

    div=-1

    for i in nodes:
        try:
            f=float(i['tasso'])
            div=nodes.index(i)
            break
        except:
            pass

    # split in 2 list

    nodes1,nodes2=nodes[:div],nodes[div:]

    # make the first dataframe from nodes

    nodes_diz1={}
    for i in range(len(nodes1)):
        temp=pd.Series(nodes1[i])
        nodes_diz1[i]=temp

    df_nodes1=pd.DataFrame(nodes_diz1).transpose()

    # make the second dataframe from nodes

    nodes_diz2={}
    for i in range(len(nodes2)):
        temp=pd.Series(nodes2[i])
        nodes_diz2[i]=temp

    df_nodes2=pd.DataFrame(nodes_diz2).transpose()

    # make the dataframe from links

    links=data["links"]

    links_diz={}
    for i in range(len(links)):
        temp=pd.Series(links[i])
        links_diz[i]=temp
        
    df_links=pd.DataFrame(links_diz).transpose()

    return df_nodes1, df_nodes2, df_links










# using the library os, I make the directory 'strutture_ospedaliere', after checking if it already exists

if not os.path.exists('strutture_ospedaliere'):
    os.makedirs('strutture_ospedaliere')

# using the library BeautifulSoup, from the html file of the web page of the all structures I extract the name of the hospital and ID number

with open("default_sintesi_stru_ajax.php.html") as fp:
    soup = BeautifulSoup(fp,"html.parser")

a_soup=soup.find_all('a',href=re.compile('sintesi_treemap2'))

# iterating for all the structures, using the self-made function request_hosp, I saved the data for all the structure into 3 tsv files

count=0
not_found=[]

for i in a_soup:
    if i.string[-2:]!='()':
        print(i.get('href').split('=')[1])
        # print(i.string)
        try:
            nodes1,nodes2,links=request_hosp('http://95.110.213.190/PNEed17/sintesi/sintesi_vis/sank/dati_gradiente_stru.php?cod_struttura='+i.get('href').split('=')[1])
            if not os.path.exists('./strutture_ospedaliere/'+i.string):
                os.makedirs('./strutture_ospedaliere/'+i.string)
                nodes1.to_csv('./strutture_ospedaliere/'+i.string+'/nodes1',sep='\t')
                nodes2.to_csv('./strutture_ospedaliere/'+i.string+'/nodes2',sep='\t')
                links.to_csv('./strutture_ospedaliere/'+i.string+'/links',sep='\t')
        except:
            count+=1
            not_found.append(i.string)

print(count)


# Thank you for the attention ==> https://www.youtube.com/watch?v=0FHEeG_uq5Y



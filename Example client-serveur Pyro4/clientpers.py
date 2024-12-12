import Pyro4
import os,pymysql,pickle,base64,random
from PIL import Image,ImageTk
from io import BytesIO

#1-Appeler le serveur pour la connection du client.
try:
    
    ns=Pyro4.locateNS()
    uri=ns.lookup('myserver')
    print(uri)
    # 2- Appel au serveur proxy
    pers=Pyro4.Proxy(uri)
    #print(pers)
    # 3 -Appeler un  objet
    x=5
    y=15
    #print(pers.Additionner(x,y))
    #print(pers.Multiplier(x,y))
    

    numerocarte='1909'
    nom='Nelson'
    prenom='Beneche'  
    numerocarte=random.randint(00000,10000)
    nom='Asa'
    prenom='Addsd'
    sexe='Masculin'
    datenaissance='2020'
    adresse='Jameau'
    telephone='49260866'
    etat_matrimoniale='Mariee'
    groupesanguin='AB'
    personneresponsable='1212121212'
    numeropersonneresponsable='hello moto'
    #asl=assure.get()
    profession='ing'
    typeassurance='maladie'
    #d=datetime.date.today()
    dateenregistrer='%d-%m-%Y'    
    with open('websit.png','rb') as f:
    
        
        str_=base64.b64encode(f.read())
        ph=str_.decode('utf-8')
        #im=Image.open(BytesIO(base64.b64decode(str_)))
        #def CreerPatient(self,numerocarte,nom,prenom,sexe,datenaissance,adresse,telephone,etat_matrimoniale,groupesanguin,personneresponsable,numeropersonneresponsable,typeassurance,profession,photo,dateenregistrer):
        connection=pymysql.connect(host='localhost',db='pharmatech',user='root',password='')   
        cur=connection.cursor()
        req=cur.execute("insert into patient values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(numerocarte,nom,prenom,sexe,datenaissance,adresse,telephone,etat_matrimoniale,groupesanguin,personneresponsable,numeropersonneresponsable,typeassurance,profession,ph,dateenregistrer))
        
        connection.commit()
        if req!=0:
            print('insertion reussie')
        else:
            print("echec d'insertion de donnnes")
        connection.close()  
        #return True        
       
       
        #print (ph)    
        #pers.SavePhoto(numerocarte,nom,prenom,ph)
        #print('reussie...')
except Pyro4.errors.ConnectionClosedError:
    print('erreur de connexion au serveur...')
    

#os.system('pause')
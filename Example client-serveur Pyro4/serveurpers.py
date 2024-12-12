import Pyro5
#import Pyro5.server
import Pyro4
import sqlite3,pymysql
@Pyro4.expose
class Personne(object): # declaration de la classe personne
    
    @Pyro4.expose #exposer le methode qui va etre appeler a distant
    def Additionner(self,x,y):
        addition=x+y
        sous=x-y
        print("l'addition est:",addition)
        connection=sqlite3.connect('remoteobjetpython.db')
        cur=connection.cursor()
        req=cur.execute('insert into addition values(?,?)',(addition,sous))
        connection.commit()
        if req!=0:
            print('Insertion de donnnes reussie.')
        else:
            print('echec')
        connection.close()    
    
    @Pyro4.expose #exposition de la methode distant que le client peut appeler
    def Multiplier(self,x,y):
        mult=x*y
        print('la multiplication est:',mult)
        
    @Pyro4.expose
    def SavePhoto(self,numerocarte,nom,prenom,ph):
        
    
        connection=pymysql.connect(host='localhost',db='pharmatech',user='root',password='')   
        cur=connection.cursor()
        req=cur.execute("insert into Essai values(%s,%s,%s,%s)",(numerocarte,nom,prenom,ph))
        
        connection.commit()
        if req!=0:
            print('insertion reussie')
        else:
            print("echec d'insertion de donnnes")
                
def main():# Fonction principale pour lancer le serveur application
    #1- faire appel a la classe daemon
    daemon=Pyro4.Daemon(host='127.0.0.1',port=1237)
    #2 -lier la classe la personne et aussi on cree le nom du serveur
    uri=daemon.register(Personne,'mathapp_clientserveur')
    print(uri)
    # 3- Le nom du serveur
    ns=Pyro4.locateNS()
    # 4-Enregistrer l'objet
    ns.register('myserver',uri)
    #5-Attente la requete du client
    print('Serveur lance')
    
    daemon.requestLoop()    
    
if __name__=='__main__':
    main()
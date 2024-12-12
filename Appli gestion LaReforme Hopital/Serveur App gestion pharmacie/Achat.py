# *-*coding :utf-8 *-*
import Pyro4
import pymysql

class Achat(object):
    
    global connection
    connection=pymysql.connect(host='localhost',password='',user='root',db='pharmatech')

    @Pyro4.expose
    def EffectuerAchat(self,id_ach,id_prod,quantite_stock,quantite_ach,date_ach):
        cur=connection.cursor()
        req=cur.execute("insert into Achat values(%s,%s,%s,%s,%s)",(id_ach,id_prod,quantite_stock,quantite_ach,date_ach))
        connection.commit()
        print("Approvisonnement de produit reussie...",id_prod)
    
    
    @Pyro4.expose
    def RechercherAchat(self,id_ach):
        cur=connection.cursor()
        req=cur.execute("select * from achat where id_ach=%s",(id_ach))
        connection.commit()
        result=cur.fetchall()
        print("Vous avez recherche un achat.")
        return result


    @Pyro4.expose
    def ListeAchatJr(self,date_ach):
        cur=connection.cursor()
        req=cur.execute("select * from achat where date_ach=%s",(date_ach))
        connection.commit()
        result=cur.fetchall()
        return result
        print("Liste des achats de la journee...")
    
         
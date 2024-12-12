import pymysql
import Pyro4
class Medicament(object):

    global connection
    connection=pymysql.connect(host='localhost', user='root', db='pharmatech', password='')
    
    @Pyro4.expose
    def AjouterMedicament(self,id_prod,description,categorie,prix,quantite,unite,dateentrer,dateperemption,composition,remarque):
        cur=connection.cursor()
        req=cur.execute("insert into Medicament values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(id_prod,description,categorie,prix,quantite,unite,dateentrer,dateperemption,composition,remarque))
        connection.commit()
        if req!=0:
            print('Un nouveau medicament a ete ajoute avec succes.')
        else:
            print("Echec d'ajout.")
            
            
    @Pyro4.expose
    
    def RechercherMedicament(self,description,unite,composition):
        cur=connection.cursor()
        req=cur.execute("select * from Medicament where description=%s and unite=%s and composition=%s",(description,unite,composition))
        connection.commit()
        resultrech=cur.fetchall()
        return resultrech

    @Pyro4.expose
    def RechercherMedicament(self, id_prod):
        cur = connection.cursor()
        req = cur.execute("select * from Medicament where id_prod=%s",(id_prod))
        connection.commit()
        resultrech = cur.fetchall()
        return resultrech

    @Pyro4.expose
    def RechercherMedicamentPourVente(self,description,unite):
        cur = connection.cursor()
        req = cur.execute("select * from Medicament where description=%s and unite=%s",(description,unite))
        connection.commit()
        resultrechvt = cur.fetchall()
        return resultrechvt

    @Pyro4.expose
    def AugmenterStockMedic(self, id_prod, quantite_ach):
        cur=connection.cursor()
        req=cur.execute("Update Medicament set quantite=quantite+"+str(quantite_ach)+" where id_prod=%s",(id_prod))
        connection.commit()
        if req!=0:
            print('Augmentation de stock de medicament:',id_prod)
        else:
            print("Echec.")

    @Pyro4.expose
    def DiminuerStockMedic(self, id_prod, quantite_v):
        cur = connection.cursor()
        req = cur.execute("Update Medicament set quantite=quantite-" + str(quantite_v) + " where id_prod=%s",(id_prod))
        connection.commit()
        if req != 0:
            print('Dimunition de stock de medicament:', id_prod)
        else:
            print("Echec.")

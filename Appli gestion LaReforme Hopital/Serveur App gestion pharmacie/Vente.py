import pymysql
import Pyro4

class Vente(object):
    global connection
    connection = pymysql.connect(host='localhost', user='root', db='pharmatech', password='')

    @Pyro4.expose
    def EffectuerVente(self,id_v,id_prod,quantite_v,prix,montant,datevente):
        cur=connection.cursor()
        req = cur.execute("insert into Vente values(%s,%s,%s,%s,%s,%s)",(id_v,id_prod,quantite_v,prix,montant,datevente))
        connection.commit()
        print("Une vente a ete effectue avec succes...code de produit vendu:", id_prod)

import tkinter
from tkinter import ttk

class Fenprincipale():
    def __init__(self):

        app = tkinter.Tk()
        app.title("Splash screen")
        app.overrideredirect(True)
        lbtit = tkinter.Label(app, text='Demarrage du client unibank')
        pr = tkinter.ttk.Progressbar(app, orient='horizontal', mode='determinate', length=200, value=100, max=100)
        pr.start(40)
        lbtit.grid(row=0, column=0)
        pr.grid(row=1, column=0)
        larg = 300
        haut = 200
        largecran = app.winfo_screenwidth()
        hautecran = app.winfo_screenheight()
        x = (largecran/2)-(larg/2)
        y = (hautecran/2)-(haut/2)
        app.geometry('%dx%d+%d+%d'%(larg, haut,x, y))

        def salut():
            app.destroy()
            fen=tkinter.Tk()
            fen.title('Connection au systeme')
            larg = 300
            haut = 200
            largecran = fen.winfo_screenwidth()
            hautecran = fen.winfo_screenheight()
            x = (largecran / 2) - (larg / 2)
            y = (hautecran / 2) - (haut / 2)
            fen.geometry('%dx%d+%d+%d' % (larg, haut, x, y))
            fen.mainloop()


        app.after(3000, salut) # faire appel a la methode salut qui va permet d'afficher une autre fenetre apres 3000 milliseconde
        app.mainloop()

if __name__=='__main__':
    Fenprincipale()

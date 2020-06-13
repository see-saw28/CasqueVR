########################
#    BIBLIOTHEQUES     #
########################

#importation des bibliotèques nécéssaires
from matplotlib.pyplot import *
import matplotlib.animation as animation #actualisation du graphe
import imageio #lecture de l'image en matrice
from numpy import *
from matplotlib.widgets import Button #utilistion de boutons
from py2duino import * #communiquer avec arduino
import time


########################
#       INTERFACE      #
########################

#conversion des fichiers images en matrices pour les 4 images
Q=imageio.imread("final_30_res.jpg")
P=imageio.imread("final_50_res.jpg")
S=imageio.imread("final_50_res-1.jpg")
R=imageio.imread("russell-westbrook1.jpg")

#ratio d'affichage des images
ratio=26/9


#nommage du graphe
fig = figure()


#création des 4 sous-graphes pour l'interfaces
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)

#suppression de l'affichage des axes pour les 4 sous-graphes
ax1.axis('off')
ax2.axis('off')
ax3.axis('off')
ax4.axis('off')

#paramétrages des axes
ax1.axis([0,ratio*len(Q),len(Q),0])#defintion des axes en fonction de la hauteur de l'image car les images 360 ont un ratio > 26/9
ax2.axis([0,ratio*len(P),len(P),0])
ax3.axis([0,len(R[0]),len(R[0])/ratio,0])#définition des axes en fonction de la largeur de l'image car l'image 2D choisie a un ratio < 26/9
ax4.axis([0,ratio*len(S),len(S),0])


#######################
#       ARDUINO       #
#######################

#definition du port usb utilisé par arduino 
ar1=Arduino(5)
    
# Affectation des axes de l'accéléromètre aux entrées analogiques
donneex=AnalogInput(ar1,0)
donneey=AnalogInput(ar1,1)
donneez=AnalogInput(ar1,2)

#fonctions permettant d'avoir un rendu plus fluide en lissant les données de l'accéléromètre
def lissagex():
    X=[]
    for i in range (0,10):#création d'une liste avec 10 valeurs de l'accéléromètre
        X.append(donneex.read())
    return mean(X)#fonction qui renvoie la valeur moyenne de la liste

def lissagey():
    Y=[]
    for i in range (0,10):#création d'une liste avec 10 valeurs de l'accéléromètre
        Y.append(donneey.read())
    return mean(Y)#fonction qui renvoie la valeur moyenne de la liste


##########################
#  FONCTIONS 2D OU 360°  #
##########################

#différents programmes car gestion différentes pour le zoom et aussi les limites pouvant être atteintes pour une image 360 ou 2D

#definition de la fonction pour une image plane(2D) 
def deuxD(M):

    #défintions des variables
    global zoom
    zoom=3
    global ratio
    ratio=16/9
    global X
    X=0
    global Y
    Y=0
    global X1
    X1=0
    global Y1
    Y1=0
    global Z1
    Z1=0
    global Z
    Z=int(len(M)/(zoom))
    global alpha
    alpha=len(M[0])-ratio*Z
    global beta
    beta=len(M)-Z
    global sigma
    sigma=int(alpha/2)
    global donneex
    global donneey
    global donneez

    
    #mise en place de l'affichage
    fig = figure()
    ax = fig.add_subplot(111)#nommage du graphe
    ax.axis('off')
    
   
    
    
    #définition des différentes fonctions
    

    
    #fonction qui permet de definir alpha et beta correspondants à la limite à ne pas dépasser pour afficher l'image
    def update():
        global zoom
        global alpha
        global beta
        Z=int(len(M)/(zoom))#hauteur de l'image à afficher en fonction du zoom
        alpha=len(M[0])-ratio*Z #largeur limite, dépendant du ratio, à ne pas dépasser lors de la définition des axes
        beta=len(M)-Z #hauteur limite à ne pas dépasser lors de la définition des axes
    
        
        
    
    #fonction qui diminue le zoom mais avec un minimum de 2   
    def down(event):
        global zoom
        
        if zoom>2:
            zoom=zoom-1
            
        update()
    
    
    #fonction qui augmente le zoom mais avec un maximum de 5  
    def up(event):
        global zoom
        
        if zoom<5:
            zoom=zoom+1
            
        update()
          
        
    def map(X,Y,V,Z):           #renvoie une valeur entre 0 et Z, proportionellement a V qui est entre X et Y
        P=int(((V-X)/(Y-X)*Z))
        return P
               
    
    
    #fonction pour actualiser l'image afficher en fonction des données de l'accéléromètre
    def animate(i):
        global X 
        global Y
        
        X1 = lissagex() #lecture des données de l'accéléromètre suivant x
        Y1 = lissagey() #lecture des données de l'accéléromètre suivant y
        X1=map(205,300,X1,alpha)#l'accéléromètre renvoie des valeurs entre 205 et 300 pour des positions entre les deux positions extrêmes
        Y1=map(300,205,Y1,beta)#inversion de 300 et 205 du fait de l'inversion de l'axe Y précisée par la suite
    
        #vérification que le cadre affiché soit bien compris dans l'image suivant x puis y
        if 0<X1<alpha: 
            X=X1
        if 0<Y1<beta:
            Y=Y1
    
        Z=int(len(M)/(zoom))#calcul de la hauteur du cadre en fonction du zoom 
        ax.axis([X,X+ratio*Z,Y+Z,Y]) #definition des dimensions du cadre pour afficher la partie de l'image souhaitée en fonction du zoom
                                     #le point (0,0) de l'image étant en haut à gauche et non en bas à gauche nécéssité d'inverser l'axe Y pour avoir une image droite
        t.set_text('Zoom : %sx'%(zoom)) #mise à jour du texte de la variable t
    
    
    
    
    
    #partie pour gerer le zoom avec des boutons
    
    
    #bouton plus
    axButton1=axes([0.025,0.35,0.1,0.1])#position
    btn1=Button(ax=axButton1,label='+',color='tomato',hovercolor='r')#definiton du bouton(position par rapport à la figure "ax",label,couleur, couleur lorsque la souris passe au dessus)
    btn1.label.set_fontsize(30)     #modification de la taille du label
    btn1.on_clicked(up)         #la fonction "up" est réalisée lors de l'appui sur le bouton
    
    #bouton moins
    axButton2=axes([0.025,0.2,0.1,0.1])
    btn2=Button(ax=axButton2,label='-',hovercolor='deepskyblue',color='skyblue')
    btn2.label.set_fontsize(50)
    btn2.on_clicked(down)
    
    
    
    
    #ESSAYER DE FAIRE UNE FONCTION POUR ALLEGER
    #gestion textes
    
    #propriétées pour les "boîtes de textes"
    props=dict(boxstyle='round4',alpha=0.2,color='r') 
    props1=dict(boxstyle='round',alpha=0.5,color='gold')
    
    #definition de la variable t correspond au texte affichant le zoom
    t=fig.text(-0.15,0.55,'Zoom : %sx '%(zoom),transform=ax.transAxes,size=20,bbox=props1)
    
    #affichage des textes supplémentaires
    fig.text(-0.18,1.1,'Projet informatique ',transform=ax.transAxes,size=12,) #affichage d'un texte(position, label, texte fixe, taille du label)
    fig.text(0.4,1.07,'Casque VR',transform=ax.transAxes,size=24,bbox=props)
    fig.text(1.02,1.05,' GAIGNE Paul \n GAYET Constant \n LEGAUD Pierre',transform=ax.transAxes,size=12,)
    fig.text(1.05,-0.12,'PCSI3',transform=ax.transAxes,size=15,)
    
    
    
    
    
    #affichage et actualisation du graphe
    
    
    ani=animation.FuncAnimation(fig,animate,interval=10) #actualisation du graphe grace a la fonction animate toutes les 5ms
    ax.imshow(M)  #affichage de la matice correspondante a l'image affichée sur la figure "ax"

    get_current_fig_manager().full_screen_toggle()#ouverture en plein écran
    show() #affichage de la fenêtre python
    
    



#definition de la fonction pour une image panoramique(360) 
def pano(M):
    global zoom
    zoom=1
    global ratio
    ratio=16/9
    global X
    X=0
    global Y
    Y=0
    global X1
    X1=0
    global Y1
    Y1=0
    global Z1
    Z1=0
    global Z
    Z=int(len(M)/(zoom))
    global alpha
    alpha=len(M[0])
    global beta
    beta=len(M)-Z
    global sigma
    sigma=int(alpha/2)#moitié de l'image nécéssaire dans la gestion du panorama cf dossier
    global donneex
    global donneey
    global donneez
    P=concatenate((M,M),axis=1)#matrice augmentée de M avec M, l'une à coté de l'autre pour assurer la transition en bout d'image 
    
    
    #mise en place de l'affichage
    fig = figure()
    ax = fig.add_subplot(111)#nommage du graphe
    ax.axis('off')
    
    
    
    
    
    #définition des différentes fonctions
    

        
    #fonction qui permet de definir alpha et beta correspondants à la limite à ne pas dépasser pour afficher l'image
    def update(): 
        global zoom
        global beta
        Z=int(len(M)/(zoom))#largeur à afficher en fonction du zoom
        beta=len(M)-Z
        
    
    
    
    #fonction qui diminue le zoom mais avec un minimum de 1   
    def down(event):
        global zoom
        global Y
    
        if zoom>1:
            zoom=zoom-1
            Y=0
        
        update()
    
    
    #fonction qui augmente le zoom mais avec un maximum de 2 car image avec ratio très grand donc zoom léger seulement
    def up(event):
        global zoom
    
        if zoom<2:
            zoom=zoom+1
        
        update()
      
    
    def map(X,Y,V,Z):           #renvoie une valeur entre 0 et Z, proportionellement a V qui est entre X et Y
        P=int(((V-X)/(Y-X)*Z))
        return P
           
    
    
    #fonction pour actualiser l'image afficher en fonction des données de l'accéléromètre
    def animate(i):
        global X
        global Y
    
        X1 = lissagex() #lecture des données de l'accéléromètre suivant x
        Y1 = lissagey() #lecture des données de l'accéléromètre suivant y
        Z1 = donneez.read() #lecture des données de l'accéléromètre suivant z
    
        if int(Z1)>250:#explication dans le dossier
            X1=map(205,300,X1,sigma)#l'accéléromètre renvoie des valeurs entre 205 et 300 pour des positions entre les deux positions extrêmes
            Y1=map(300,205,Y1,beta)#inversion de 300 et 205 du fait de l'inversion de l'axe Y précisée par la suite
    
        else :
            X1=(sigma + map(300,200,X1,sigma))#l'accéléromètre renvoie des valeurs entre 205 et 300 pour des positions entre les deux positions extrêmes
            Y1=map(200,300,Y1,beta)#inversion de 300 et 205 du fait de l'inversion de l'axe Y précisée par la suite
    
    
    #vérification que le cadre affiché soit bien compris dans l'image suivant x puis y
        if 0<X1<alpha: 
            X=X1
        if 0<Y1<beta:
            Y=Y1
    
        Z=int(len(M)/(zoom))#calcul de la hauteur du cadre en fonction du zoom 
        ax.axis([X,X+ratio*Z,Y+Z,Y]) #definition des dimensions du cadre pour afficher la partie de l'image souhaitée en fonction du zoom
                                 #le point (0,0) de l'image étant en haut à gauche et non en bas à gauche nécéssité d'inverser l'axe Y pour avoir une image droite
        t.set_text('Zoom : %sx'%(zoom)) #mise à jour du texte de la variable t
    
    
    
    
    
    #partie pour gerer le zoom avec des boutons
    
    
    #bouton plus
    axButton1=axes([0.03,0.35,0.1,0.1])#position
    btn1=Button(ax=axButton1,label='+',color='tomato',hovercolor='r')#definiton du bouton(position par rapport à la figure "ax",label,couleur, couleur lorsque la souris passe au dessus)
    btn1.label.set_fontsize(30)     #modification de la taille du label
    btn1.on_clicked(up)         #la fonction "up" est réalisée lors de l'appui sur le bouton
    
    #bouton moins
    axButton2=axes([0.03,0.2,0.1,0.1])#position
    btn2=Button(ax=axButton2,label='-',hovercolor='deepskyblue',color='skyblue')#definiton du bouton(position par rapport à la figure "ax",label,couleur, couleur lorsque la souris passe au dessus)
    btn2.label.set_fontsize(50)#modification de la taille du label
    btn2.on_clicked(down)#la fonction "down" est réalisée lors de l'appui sur le bouton
    
    
    
    
    
    #gestion textes
    
    #propriétées pour les "boîtes de textes"
    props=dict(boxstyle='round4',alpha=0.2,color='r') 
    props1=dict(boxstyle='round',alpha=0.5,color='gold')
    
    #definition de la variable t correspond au texte affichant le zoom
    t=fig.text(-0.15,0.55,'Zoom : %sx '%(zoom),transform=ax.transAxes,size=20,bbox=props1)
    
    #affichage des textes supplémentaires
    fig.text(-0.18,1.1,'Projet informatique ',transform=ax.transAxes,size=12,) #affichage d'un texte(position, label, texte fixe, taille du label)
    fig.text(0.4,1.07,'Casque VR',transform=ax.transAxes,size=24,bbox=props)
    fig.text(1.02,1.05,' GAIGNE Paul \n GAYET Constant \n LEGAUD Pierre',transform=ax.transAxes,size=12,)
    fig.text(1.05,-0.12,'PCSI3',transform=ax.transAxes,size=15,)
    
    
    
    
    
    #affichage et actualisation du graphe
    
    
    ani=animation.FuncAnimation(fig,animate,interval=10) #actualisation du graphe grace a la fonction animate toutes les 10ms
    ax.imshow(P)  #affichage de la matice correspondante a l'image affichée sur la figure "ax"

    get_current_fig_manager().full_screen_toggle()#ouverture en plein écran
    show() #affichage de la fenêtre python
    

###########################
#   RETOUR A L'INTERFACE  #
###########################


#définitions des fonctions appelant la fonction voulue (2d ou 360) avec la matrice correspondante
def p(event):
    pano(P)

def q(event):
    pano(Q)

def r(event):
    deuxD(R)

def s(event):
    pano(S)
    


#création des boutons de l'interface

axButton1=axes([0.25,0.45,0.1,0.1])#position
btn1=Button(axButton1,label='Quebec',color='lightgrey',hovercolor='greenyellow')#definiton du bouton(position par rapport à la figure "ax",label,couleur, couleur lorsque la souris passe au dessus)
btn1.label.set_fontsize(20)     #modification de la taille du label
btn1.on_clicked(q)         #appel de la fonction souhaitée lors de l'appui sur le bouton

axButton2=axes([0.68,0.45,0.1,0.1])#position
btn2=Button(axButton2,label='Place',color='lightgrey',hovercolor='greenyellow')#definiton du bouton(position par rapport à la figure "ax",label,couleur, couleur lorsque la souris passe au dessus)
btn2.label.set_fontsize(20)     #modification de la taille du label
btn2.on_clicked(p)         #appel de la fonction souhaitée lors de l'appui sur le bouton

axButton3=axes([0.25,0.05,0.1,0.1])#position
btn3=Button(axButton3,label='Westbrook',color='lightgrey',hovercolor='greenyellow')#definiton du bouton(position par rapport à la figure "ax",label,couleur, couleur lorsque la souris passe au dessus)
btn3.label.set_fontsize(20)     #modification de la taille du label
btn3.on_clicked(r)         #appel de la fonction souhaitée lors de l'appui sur le bouton

axButton4=axes([0.68,0.05,0.1,0.1])#position
btn4=Button(axButton4,label='Salon',color='lightgrey',hovercolor='greenyellow')#definiton du bouton(position par rapport à la figure "ax",label,couleur, couleur lorsque la souris passe au dessus)
btn4.label.set_fontsize(20)     #modification de la taille du label
btn4.on_clicked(s)         #appel de la fonction souhaitée lors de l'appui sur le bouton

#affichage des textes supplémentaires

props=dict(boxstyle='square',alpha=0.2,color='r')        
fig.text(0.01,0.98,'Projet informatique ',size=12,) #affichage d'un texte(position, label, taille du label)
fig.text(0.38,0.9,'Selectionnez une image',size=24,bbox=props)#affichage d'un texte(position, label, taille du label,propriétés du cadre)
fig.text(0.9,0.92,' GAIGNE Paul \n GAYET Constant \n LEGAUD Pierre',size=12,)#affichage d'un texte(position, label, taille du label)
fig.text(0.95,0.03,'PCSI3',size=15,)#affichage d'un texte(position, label, taille du label)



#affichage des matrices des images dans chacun des sous-graphes de l'interface
ax1.imshow(Q)
ax2.imshow(P)
ax3.imshow(R)
ax4.imshow(S)

get_current_fig_manager().full_screen_toggle()
#affichage du graphe
show()

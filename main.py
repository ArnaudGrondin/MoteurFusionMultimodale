#from tkinter import *
#from tkinter import ttk
#import tkinter as tk
import ivy.std_api as ivyapi
import simple
import fusion_engine
import sys
import pygame
from pygame import Rect,Surface
from forme import Forme
#ivyapi.IvyInit("interface")
#ivyapi.IvyStart()
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
''' Interface multimodale'''

def sum_tuple(t1,t2):
    return tuple(map(sum,(zip(t1,t2))))

liste_forme = list()
id_forme = 0
# fonction qui dessine les formes a l'écran 
def dessiner_forme(fenetre,nom_forme,liste_forme,coord=(210,180), couleur =(255,0,0) ):
    rect = Rect(coord,(180,200))
    global id_forme
    match nom_forme:
        case 'RECTANGLE':
            r = pygame.draw.rect(fenetre,couleur,rect)
            f = Forme( id_forme,nom_forme,couleur,coord)
            print(f"{r}") # <rect(210, 180, 180, 200)>
            liste_forme.append(f)
            #liste_forme.add(pygame.draw.circle(fenetre,(0,255,0),))
            id_forme += 1
        case 'CIRCLE':
            pygame.draw.circle(fenetre,(0,255,0),coord,20.0)
            f = Forme(id_forme,nom_forme,couleur,20.5)
            liste_forme.append(f)
            id_forme += 1
        case 'DIAMOND':
            diamond_points = [sum_tuple(coord,(50,0)),sum_tuple(coord,(-50,0)), sum_tuple(coord,(0,-50)), sum_tuple(coord,(0,50))] # coord sommet haut,bas,gauche,droite
            pygame.draw.polygon(fenetre,couleur,diamond_points)
            f = Forme(id_forme,nom_forme,couleur,coord)
            liste_forme.append(f)
            id_forme += 1
        case 'TRIANGLE':
            triangle_points = [sum_tuple(coord,(50,0)), sum_tuple(coord,(-50,-50)), sum_tuple(coord,(-50,50))] # coord sommet haut,gauche,droite 
            pygame.draw.polygon(fenetre,couleur,triangle_points)
            f = Forme(id_forme,nom_forme,couleur,coord)
            liste_forme.append(f)
            id_forme += 1
        case _:
            pass
def effacer_forme(forme,coord):
    #cherchez avec pygame s'il y a une forme aux coordonées spécifiées

    # vérifier que la forme a supprimé correspond à ce qui est dit a l'oral 
    pass
    
def redraw_form_list():
    for f in liste_forme:
        dessiner_forme

def main():
    pygame.init()
    liste_cmd = list()
    fenetre = pygame.display.set_mode((800, 600))
    running = True
    clock = pygame.time.Clock()
    motor = fusion_engine.FusionMotor()
    font = pygame.font.SysFont(None, 32)
    fenetre.fill("white")
    
    coord_mouse = (0,0)

    while running:
        dt = clock.tick(60) #/ 1000 #limite les fps a 60
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                coord_mouse = pygame.mouse.get_pos() # A enlever si IVY marche
                ivyapi.IvySendMsg("mouse: "+str(coord_mouse))
                
                pass
        action = ""
        if len(motor.sra5_token) > 3 : #todo rajouter une condition sur le taux de confiance
            score = float( motor.sra5_dict['Confidence'].replace(',','.'))
            if score > 0.6 : # tous les champs doivent être remplis

                #print(float(score))
                #print(f"{motor.sra5_dict}")
                liste_cmd.append(motor.sra5_dict) # on veut un historique des commandes
                action = motor.sra5_dict['action']
                match action:
                    case 'CREATE':
                        dessiner_forme(fenetre,motor.sra5_dict['form'],liste_forme)
                    case 'MOVE':
                        pass
                    case 'DELETE':
                        fenetre.fill("white")
                        pass
                    case 'QUIT':
                        pass 
                pygame.display.flip()
                
            #print("yes " + text )

        # print("Token " + str(len(motor.sra5_token)) )
        #print("String " + motor.sra5_string)
        text_surface = font.render(action, True, (255, 255, 255), (0, 0, 0))
        # rend les informations graphiques à l'écran 

        fenetre.blit(text_surface, (20, 20))
        pygame.display.flip()
        
        
    # Gestion des événements
    # ...

    # Rafraîchissement de l'écran
    

    # Fermeture de Pygame
    pygame.quit()
    sys.exit()
    # app = interface()
    # app.master.title('Interface multimodale')
    #app.mainloop()
    #
    
    
if __name__ == "__main__" :
    main()

#from tkinter import *
#from tkinter import ttk
#import tkinter as tk
import ivy.std_api as ivyapi
import simple
import fusion_engine
import sys
import pygame
from pygame import Rect,Surface
import os
#ivyapi.IvyInit("interface")
#ivyapi.IvyStart()
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
''' Interface multimodale'''

liste_forme = list()

# fonction qui dessine les formes a l'écran 
def dessiner_forme(fenetre,forme,liste_forme,coord=(210,180), couleur =(255,0,0) ):
    rect = Rect(coord,(180,200))
    
    match forme:
        case 'RECTANGLE':
            r = pygame.draw.rect(fenetre,couleur,rect)
            print(f"{r}") # <rect(210, 180, 180, 200)>
            #liste_forme.append()
            #liste_forme.add(pygame.draw.circle(fenetre,(0,255,0),))
        case 'CIRCLE':
            pygame.draw.circle(fenetre,(0,255,0),1.5)
            #liste_forme.append() 
            pass
        case 'DIAMOND':
            diamond_points = [coord + (50,0),coord + (-50,0), coord + (0,-50),coord + (0,50)] # coord sommet haut,bas,gauche,droite
            pygame.draw.circle(fenetre,couleur,diamond_points)
            pass
        case 'TRIANGLE':
            triangle_points = [coord + (50,0), coord + (-50,-50),coord + (-50,50)] # coord sommet haut,gauche,droite 
            liste_forme.append(pygame.draw.polygon(fenetre,couleur,triangle_points))
            pass
        case _:
            pass
def effacer_forme(forme,coord):
    #cherchez avec pygame s'il y a une forme aux coordonées spécifiées

    # vérifier que la forme a supprimé correspond à ce qui est dit a l'oral 
    pass
    
def redraw_form_list():
    for f in liste_forme:
        pygame.draw(f)

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
            if score > 0.6:

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

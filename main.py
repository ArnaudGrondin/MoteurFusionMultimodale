#from tkinter import *
#from tkinter import ttk
#import tkinter as tk
import ivy.std_api as ivyapi
import simple
import time
import ast
import sys
import pygame
from pygame import Rect,Surface
from forme import Forme
import threading
ivyapi.IvyInit("interface", "hi", 0)
ivyapi.IvyStart()
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
''' Interface multimodale'''


fusion= None
def sum_tuple(t1,t2):
    return tuple(map(sum,(zip(t1,t2))))


def fusion_engine_callback(agent,arg)-> None:
    global fusion
    fusion = ast.literal_eval(arg)

ivyapi.IvyBindMsg(fusion_engine_callback,"^fusion_engine: (.*)")

liste_forme = []
id_forme = 0
# fonction qui dessine les formes a l'écran 
def draw_form(fenetre,nom_forme,coord=(210,180), couleur =(255,0,0) ):
    rect = Rect(coord,(180,200))
    global id_forme
    global liste_forme
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
            f = Forme(id_forme,nom_forme,couleur,coord)
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

def remove_form(coord_mouse):
    min_dist = float('inf')
    forme_to_delete = None
    for f in liste_forme:
        dist = ((f.coord[0] - coord_mouse[0])**2 + (f.coord[1] - coord_mouse[1])**2)**0.5
        if dist < min_dist:
            min_dist = dist
            forme_to_delete = f
    if forme_to_delete is not None:
        liste_forme.remove(forme_to_delete)
    # vérifier que la forme a supprimé correspond à ce qui est dit a l'oral 

def move_form(coord_mouse):
    coord2 = None
    min_dist = float("inf")
    forme_to_move = None
    for f in liste_forme:
        dist = (
            (f.coord[0] - coord_mouse[0]) ** 2 + (f.coord[1] - coord_mouse[1]) ** 2
        ) ** 0.5
        if dist < min_dist:
            min_dist = dist
            forme_to_move = f
    if forme_to_move is not None:
        liste_forme.remove(forme_to_move)
        print("choisissez la nouvelle position")
        while coord2 is None:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    coord2 = event.pos
        forme_to_move.coord = coord2
        liste_forme.append(forme_to_move)
        coord2 = None

def redraw_form_list(fenetre):
    for forme in liste_forme:
        match forme.nom_forme:
            case 'RECTANGLE':
                rect = Rect(forme.coord, (180, 200))
                pygame.draw.rect(fenetre, forme.couleur, rect)
            case 'CIRCLE':
                pygame.draw.circle(fenetre, forme.couleur, forme.coord, 20)
            case 'DIAMOND':
                diamond_points = [
                    sum_tuple(forme.coord, (50, 0)), sum_tuple(forme.coord, (-50, 0)),
                    sum_tuple(forme.coord, (0, -50)), sum_tuple(forme.coord, (0, 50))
                ]
                pygame.draw.polygon(fenetre, forme.couleur, diamond_points)
            case 'TRIANGLE':
                triangle_points = [
                    sum_tuple(forme.coord, (50, 0)), sum_tuple(forme.coord, (-50, -50)),
                    sum_tuple(forme.coord, (-50, 50))
                ]
                pygame.draw.polygon(fenetre, forme.couleur, triangle_points)

def main():
    pygame.init()
    liste_cmd = list()
    fenetre = pygame.display.set_mode((800, 600))
    running = True
    clock = pygame.time.Clock()
    # motor = fusion_engine.FusionMotor()
    font = pygame.font.SysFont(None, 32)
    fenetre.fill("white")
    global fusion
    
    coord_mouse = (0,0)
    global liste_forme
    while running:
        dt = clock.tick(60) #/ 1000 #limite les fps a 60
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                coord_mouse = pygame.mouse.get_pos() # A enlever si IVY marche
                ivyapi.IvySendMsg("mouse: "+str(coord_mouse))
                print(coord_mouse)
                
        action = ""
        # if len(motor.sra5_token) > 3 : #todo rajouter une condition sur le taux de confiance
        if fusion is not None:
            score = float(fusion['Confidence'].replace(',','.'))
            if score > 0.6 : # tous les champs doivent être remplis
                
            
            
            
            
            # liste_cmd.append(motor.sra5_dict) # on veut un historique des commandes
                action = fusion['action']
                forme = fusion['form']
                match action:
                    case 'CREATE':
                        draw_form(fenetre,forme, coord_mouse)
                        time.sleep(1)
                    case 'MOVE':
                        move_form(coord_mouse)
                        time.sleep(1)
                    case 'DELETE':
                        remove_form(coord_mouse)
                        time.sleep(1)      
                    case 'QUIT':
                        pass
                    case _:
                        pass
                pygame.display.flip()
            
        #print("yes " + text )

        redraw_form_list(fenetre)
        text_surface = font.render(action, True, (255, 255, 255), (0, 0, 0))
        # rend les informations graphiques à l'écran 
        
        fenetre.blit(text_surface, (20, 20))
        pygame.display.flip()
        fusion = None
        fenetre.fill("white")
    
    

    
    

    # Fermeture de Pygame
    pygame.quit()
    sys.exit()
    # app = interface()
    # app.master.title('Interface multimodale')
    #app.mainloop()
    #
    
    
if __name__ == "__main__" :
    main()

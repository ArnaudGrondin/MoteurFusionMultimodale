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
   
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
''' Interface multimodale'''
# class interface():

#     self.root = Tk()

#     def __init__():
#         tk.Frame.__init__(self, master)
#         self.grid(padding="3 3 12 12")                 
#         self.size()      
#         self.createWidgets()

#     def createWidgets(self):
#         self.quitButton = tk.Button(self, text='Quit',command=self.quit)            
#         self.quitButton.grid()    

def dessiner_forme(fenetre,forme,coord=(210,180), couleur =(255,0,0) ):
    rect = Rect(coord,(180,200))

    match forme:
        case 'RECTANGLE':
            pygame.draw.rect(fenetre,couleur,rect)
        case 'CIRCLE':
            pass
        case 'DIAMOND':
            pass
        case 'TRIANGLE':
            pass
        case _:
            pass

def main():
    pygame.init()
    liste_cmd = list()
    fenetre = pygame.display.set_mode((800, 600))
    running = True
    clock = pygame.time.Clock()
    motor = fusion_engine.FusionMotor()
    font = pygame.font.SysFont(None, 32)
    fenetre.fill("white")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        action = ""
        if len(motor.sra5_token) > 3 : #todo rajouter une condition sur le taux de confiance
            score = float( motor.sra5_dict['Confidence'].replace(',','.'))
            if score > 0.6:

                #print(float(score))
                print(f"{motor.sra5_dict}")
                liste_cmd.append(motor.sra5_dict) # on veut un historique des commandes
                action = motor.sra5_dict['action']
                forme = motor.sra5_dict['form']
                dessiner_forme(fenetre,forme)
            #print("yes " + text )

       # print("Token " + str(len(motor.sra5_token)) )
        #print("String " + motor.sra5_string)
        text_surface = font.render(action, True, (255, 255, 255), (0, 0, 0))
        # rend les informations graphiques à l'écran 
        fenetre.blit(text_surface, (20, 20))
        pygame.display.flip()
        dt = clock.tick(10) / 1000 #limite les fps a 60
        
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

#from tkinter import *
#from tkinter import ttk
#import tkinter as tk
import ivy.std_api as ivyapi
import simple
import fusion_engine
import sys
import pygame
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

def main():
    pygame.init()
    fenetre = pygame.display.set_mode((800, 600))
    running = True
    clock = pygame.time.Clock()
    motor = fusion_engine.FusionMotor()
    font = pygame.font.SysFont(None, 32)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        fenetre.fill("white")
        #texte = str( motor.forme)
        print(motor.sra5_callback)
       # print("Token " + str(len(motor.sra5_token)) )
        print("String " + motor.sra5_string)
        text_surface = font.render("texte", True, (255, 255, 255), (0, 0, 0))
        # rend les informations graphiques à l'écran 
        fenetre.blit(text_surface, (20, 20))
        pygame.display.flip()
        dt = clock.tick(60) / 1000 #limite les fps a 60
        
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

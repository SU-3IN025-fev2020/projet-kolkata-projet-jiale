# -*- coding: utf-8 -*-

# Nicolas, 2020-03-20

from __future__ import absolute_import, print_function, unicode_literals
from gameclass import Game,check_init_game_done
from spritebuilder import SpriteBuilder
from players import Player
from sprite import MovingSprite
from ontology import Ontology
from itertools import chain
import pygame
import glo

import random
import numpy as np
import sys




# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None):
    global player,game
    # pathfindingWorld_MultiPlayer4
    name = _boardname if _boardname is not None else 'kolkata_6_10'
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 5  # frames per second
    game.mainiteration()
    game.mask.allow_overlaping_players = True
    player = game.player


class noeud():

    def __init__(self, parent, position):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0
    def getParent(self):
        return self.parent


    def getPosition(self):
        return self.position



def astar(map,Debutjoueur,restaurant):


    DNoeud = noeud(None,Debutjoueur)
    DNoeud.g = DNoeud.f = DNoeud.h = 0

    Grestaurant = noeud(None,restaurant)

    Grestaurant.g = Grestaurant.h = Grestaurant.f = 0


    #on initialise deux listes pour mettre a jour le chemin possible et chemin choisis

    list1 = []
    list1.append(DNoeud)



    list2 = []




    # on parcours jusqu'a on trouve le restaurant destiné
    while len(list1) > 0:
        #recuperation de noeud actuel
        current_noeud = list1[0]
        current_index = 0


        for index,posj in enumerate(list1): #on utilise enumerate() pour recupere index
            if posj.f < current_noeud.f:
                current_noeud = posj
                current_index = index

        list1.pop(current_index) #on l'enleve dans les possiblités
        list2.append(current_noeud) # on l'ajoute dans le chemin

        if current_noeud == Grestaurant:
            chemin = []
            cible = current_noeud
            while current is not None:
                chemin.append(cible.position)
                cible = current.parent
            return chemin[::-1] #remets le chemin trouvé dans le bon sens




    #creation des branches fils
    fils = []

    for prochaine in [(0,-1),(0,1),(-1,0),(1,0)]: #on prend les 4 cases autour de la position

        noeud_position = (current_noeud.position[0] + prochaine[0],current_noeud.position[1]+prochaine[1])


        new_noeud = noeud(current_noeud,noeud_position)

        fils.append(new_noeud)



    for objet in fils:

        #on verifie si le fils est dans le liste de chemin emprunté
        for set2 in list2:
            if objet == set2:
                continue




        objet.g = current_noeud.g + 1 # on ajoute le cout par 1
        objet.h = abs(objet.position[0] - Grestaurant.position[0]) + abs(objet.position[1] - Grestaurant.position[1]) # valeur heuristique en positive
        objet.f = objet.g + objet.h


        #on verifie si le fils est deja dans la liste des chemin possible
        for set1 in list1:
            if objet == set1 and objet.g > set1.g:
                continue


        list.append(objet)

def main():

    #for arg in sys.argv:
    iterations = 20 # default
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print ("Iterations: ")
    print (iterations)

    init()





    #-------------------------------
    # Initialisation
    #-------------------------------
    nbLignes = game.spriteBuilder.rowsize
    nbColonnes = game.spriteBuilder.colsize
    print("lignes", nbLignes)
    print("colonnes", nbColonnes)


    players = [o for o in game.layers['joueur']]
    nbPlayers = len(players)


    # on localise tous les états initiaux (loc du joueur)
    initStates = [o.get_rowcol() for o in game.layers['joueur']]
    print ("Init states:", initStates)


    # on localise tous les objets  ramassables (les restaurants)
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
    print ("Goal states:", goalStates)
    nbRestaus = len(goalStates)

    # on localise tous les murs
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
    #print ("Wall states:", wallStates)

    # on liste toutes les positions permises
    allowedStates = [(x,y) for x in range(nbLignes) for y in range(nbColonnes)\
                     if (x,y) not in wallStates or  goalStates]

    #-------------------------------
    # Placement aleatoire des joueurs, en évitant les obstacles
    #-------------------------------

    posPlayers = initStates


    for j in range(nbPlayers):
        x,y = random.choice(allowedStates)
        players[j].set_rowcol(x,y)
        game.mainiteration()
        posPlayers[j]=(x,y)





    #-------------------------------
    # chaque joueur choisit un restaurant
    #-------------------------------

    restau=[0]*nbPlayers
    for j in range(nbPlayers):
        c = random.randint(0,nbRestaus-1)
        print(c)
        restau[j]=c

    #-------------------------------
    # Boucle principale de déplacements
    #-------------------------------

    for i in range(iterations):


        for j in range(nbPlayers):
            score = []
            score[j] = 0
            row,col = posPlayers[j]

            res = astar(game,posPlayers[j],restau[j])


            for chemin in res:
                x_inc,y_inc= posPlayers[chemin]
                next_row = row + x_inc
                next_col = col + y_inc
                if ((next_row,next_col) not in wallStates) and next_row>=0 and next_row<=19 and next_col>=0 and next_col<=19:
                    players[j].set_rowcol(next_row,next_col)
                    print ("pos :", j, next_row,next_col)
                    game.mainiteration()

                    col=next_col
                    row=next_row
                    posPlayers[j]=(row,col)

                if (row,col) == restau[j]:
                  o = players[j].ramasse(game.layers)
                  game.mainiteration()
                  print ("Le joueur ", j, " est à son restaurant.")
                  score[j]+=1
                  print("Le joueur ", j, "a desormais le socre",socre[j])
                  goalStates.remove((row,col))


                  break



"""

    # bon ici on fait juste plusieurs random walker pour exemple...

    for i in range(iterations):

        for j in range(nbPlayers): # on fait bouger chaque joueur séquentiellement
            row,col = posPlayers[j]

            x_inc,y_inc = random.choice([(0,1),(0,-1),(1,0),(-1,0)])
            next_row = row+x_inc
            next_col = col+y_inc
            # and ((next_row,next_col) not in posPlayers)
            if ((next_row,next_col) not in wallStates) and next_row>=0 and next_row<=19 and next_col>=0 and next_col<=19:
                players[j].set_rowcol(next_row,next_col)
                print ("pos :", j, next_row,next_col)
                game.mainiteration()

                col=next_col
                row=next_row
                posPlayers[j]=(row,col)


            # si on est à l'emplacement d'un restaurant, on s'arrête
            if (row,col) == restau[j]:
                o = players[j].ramasse(game.layers)
                game.mainiteration()
                print ("Le joueur ", j, " est à son restaurant.")
                goalStates.remove((row,col)) # on enlève ce goalState de la liste


                break
"""
pygame.quit()





if __name__ == '__main__':
    main()




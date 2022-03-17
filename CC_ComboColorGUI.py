# ==============================================================================
"""ComboColor : Create the Combo Color game"""
# ==============================================================================
__author__  = "Tristan Gonçalves, Terry Bouchez"
__version__ = "3.0"   # GUI connecté au Kernel.
__date__    = "02/01/2020"
# ------------------------------------------------------------------------------
from ezTK import *
from ezCLI import read_txt, write_txt
from PIL import Image, ImageDraw, ImageTk
from CC_KernelComboColor import KernelComboColor
from datetime import datetime as dt
# ------------------------------------------------------------------------------
class ComboColorGUI(Win):
    """GUI class for the ComboColor game"""
# --------------------------------------------------------------------------
    def __init__(self, player1 = 'Player 1', player2 = 'Player 2'):
        """creation of the main window and packing gadgets"""
        self.__count = 0
        # Alternance des couleurs des joueurs, Rouge,Vert,Bleu,Jaune
        #                             Joueur   1(A)  2(B) 1(A) 2(B)
        self.colors = ((255,0,0),(0,255,0),(0,0,255),(239,239,0)) 
        Win.__init__(self, title='ComboColor', op=0, grow=False, border = 0, click=self.on_click) 
  # ---------------------------------------------------------------------------
        self.board   = Image.new('RGB', (699,699)) # create empty PIL image
        self.boardtk = ImageTk.PhotoImage(self.board)  # create empty TK image

        self.config = Frame(self, op = 2, flow='SE') #Global Frame

        self.choose_players = Frame(self.config, flow='ES', fold=2)
        self.name_p1  = Label(self.choose_players, text='Player 1 :', font='Arial 18 bold')
        self.name_p2  = Label(self.choose_players, text='Player 2 :', font='Arial 18 bold')
        self.entry_p1 = Entry(self.choose_players, width=10, command = self.on_entry, bg='White') 
        self.entry_p2 = Entry(self.choose_players, width=10, command = self.on_entry, bg='White')

        self.configA = Frame(self.config, flow='SE')
        self.label   = Label(self.configA, text='Choose a level', font='Arial 18 bold')
        self.configB = Frame(self.configA, flow='ES', fold=3) #Frame for the buttons
        
        Button (self.configB, text = 'A',  width = 10, command=lambda : self.on_entry('A', self.entry_p1(),self.entry_p2()))
        Button (self.configB, text = 'B',  width = 10, command=lambda : self.on_entry('B', self.entry_p1(),self.entry_p2()))
        Button (self.configB, text = 'C',  width = 10, command=lambda : self.on_entry('C', self.entry_p1(),self.entry_p2()))
        Button (self.configB, text = 'D',  width = 10, command=lambda : self.on_entry('D', self.entry_p1(),self.entry_p2()))
        Button (self.configB, text = 'E',  width = 10, command=lambda : self.on_entry('E', self.entry_p1(),self.entry_p2()))
        Button (self.configB, text = 'F',  width = 10, command=lambda : self.on_entry('F', self.entry_p1(),self.entry_p2()))
        Button (self.configB, text = 'HELP',  width = 10, command = HelpWin)

  # --------------------------------------------------------------------------
        self.player1 = player1
        self.player2 = player2
        self.loop()
  # ----------------------------------------------------------------------------
    def on_entry(self, selected_lvl, player1,player2):
        """callback function for the players names entry"""
        # Si Nom du Player 1 indiqué : conserver l'entry
        if len(self.entry_p1()) != 0 : self.player1 = self.entry_p1()
        # Si Nom du Player 2 indiqué : conserver l'entry
        if len(self.entry_p2()) != 0 : self.player2 = self.entry_p2()
        # Si un des deux noms pas inscrit : remplacé par Player [n°]
        self.start(selected_lvl, self.player1, self.player2)

  # ----------------------------------------------------------------------------
    def start(self, selected_lvl, player1, player2):
        """callback function for the level selector button"""
        self.game = KernelComboColor(selected_lvl) # démarrer le noyau
        self.config.destroy()
        # Créer les Frame pour chaque joueur
        self.players_frame = Frame(self, font = 'Arial 18 ', op = 3, fold = 2) 
        self.players_frame1 = Frame(self.players_frame, font = 'Arial 18 ', op = 3, fold = 2, border = 2, relief ='ridge')
        self.players_frame2 = Frame(self.players_frame, font = 'Arial 18 ', op = 3, fold = 2, border = 2, relief ='ridge')
        # Player 1
        self.player1_frame = Label(self.players_frame1, text=player1)
        self.score_p1 = Label(self.players_frame1, text=0)
        # Player 2
        self.player2_frame = Label(self.players_frame2, text=player2)
        self.score_p2 = Label(self.players_frame2, text=0)
        

        # read images from disk and create associated widget board
        self.board = Image.open(f"Boards/board{selected_lvl}.png")
        self.boardtk = ImageTk.PhotoImage(self.board)
        # label contenant l'image
        self.label = Label(self, image = self.boardtk, border = 0)
        Button (self, text = 'HELP',  width = 10, command= HelpWin)

  # ----------------------------------------------------------------------------
  # ----------------------------------------------------------------------------
    def on_click(self,widget,code,mods):
        """callback function for the click event"""
        if widget != self.label: return # only click on board are processed
        x = (widget.winfo_pointerx() - widget.winfo_rootx()) # get x coord for mouse 
        y = (widget.winfo_pointery() - widget.winfo_rooty()) # get y coord for mouse
        coord_pix = (x,y)
        cols = x//63
        rows = y//63
        
        # getpixel donne la value du pixel sur lequel on clique
        if (x//63, y//63) != (5,5): # ne colorie pas la case du centre
            if self.board.getpixel((x,y)) == (255,255,255) : # Ne peut colorier que les cases blanches
                # ---------------------- Localisation : centre --------------------------------------           
                if cols not in {0,10} and rows not in {0,10}: # si on n'est pas sur les bords de l'image
                    if self.game.levelboard[rows][cols-1] in self.game.zones_coloriees\
                       or self.game.levelboard[rows][cols+1] in self.game.zones_coloriees \
                       or self.game.levelboard[rows-1][cols] in self.game.zones_coloriees \
                       or self.game.levelboard[rows+1][cols] in self.game.zones_coloriees :                   
                        ImageDraw.floodfill(self.board,coord_pix, self.colors[self.__count%4])
                        self.boardtk.paste(self.board)
                        self.game.scores(cols,rows,self.__count%4) # appel de la méthode score du noyau
                        self.__count +=1
                        self.display()   # appel de display pour mettre à jour les scores

                # ---------------------- Localisation : coin --------------------------------------           
                elif cols in {0,10} and rows in {0,10}: # si on est dans un des coins

                    if cols == 0 and rows == 0: #en haut à gauche
                        if self.game.levelboard[rows][cols+1] in self.game.zones_coloriees  \
                           or self.game.levelboard[rows+1][cols] in self.game.zones_coloriees:
                            ImageDraw.floodfill(self.board,coord_pix, self.colors[self.__count%4])
                            self.boardtk.paste(self.board) 
                            self.game.scores(cols,rows,self.__count%4) #appel de la méthode score du noyau
                            self.display()   # appel de display pour mettre à jour les scores      
                            self.__count +=1

                    elif cols == 10 and rows == 0: #en haut à droite
                        if self.game.levelboard[rows][cols-1] in self.game.zones_coloriees  \
                           or self.game.levelboard[rows+1][cols] in self.game.zones_coloriees:
                            ImageDraw.floodfill(self.board,coord_pix, self.colors[self.__count%4])
                            self.boardtk.paste(self.board)
                            self.game.scores(cols,rows,self.__count%4) 
                            self.__count +=1
                            self.display()   
                    elif cols == 0 and rows == 10: #en bas à gauche
                        if self.game.levelboard[rows][cols+1] in self.game.zones_coloriees  \
                           or self.game.levelboard[rows-1][cols] in self.game.zones_coloriees:
                            ImageDraw.floodfill(self.board,coord_pix, self.colors[self.__count%4])
                            self.boardtk.paste(self.board)
                            self.game.scores(cols,rows,self.__count%4)
                            self.__count +=1
                            self.display()   
                    elif cols == 10 and rows == 10: #en bas à droite
                        if self.game.levelboard[rows][cols-1] in self.game.zones_coloriees  \
                           or self.game.levelboard[rows-1][cols] in self.game.zones_coloriees:
                            ImageDraw.floodfill(self.board,coord_pix, self.colors[self.__count%4])
                            self.boardtk.paste(self.board)
                            self.game.scores(cols,rows,self.__count%4) 
                            self.__count +=1
                            self.display()   

                # ---------------------- Localisation : bord --------------------------------------           
                elif cols in {0,10} or rows in {0,10}: #si on est dans un des bords 
                    if cols == 0 : # bord de gauche
                        # verif à droite  # verif au dessus  # verif en dessous
                        if self.game.levelboard[rows][cols+1] in self.game.zones_coloriees   \
                           or self.game.levelboard[rows-1][cols] in self.game.zones_coloriees\
                           or self.game.levelboard[rows+1][cols] in self.game.zones_coloriees:
                            ImageDraw.floodfill(self.board,coord_pix, self.colors[self.__count%4])
                            self.boardtk.paste(self.board)
                            self.game.scores(cols,rows,self.__count%4)
                            self.__count +=1
                            self.display()   
                            
                    elif cols == 10 : # bord de droite
                        if self.game.levelboard[rows][cols-1] in self.game.zones_coloriees\
                           or self.game.levelboard[rows-1][cols] in self.game.zones_coloriees\
                           or self.game.levelboard[rows+1][cols] in self.game.zones_coloriees:
                            ImageDraw.floodfill(self.board,coord_pix, self.colors[self.__count%4])
                            self.boardtk.paste(self.board)
                            self.game.scores(cols,rows,self.__count%4) 
                            self.__count +=1
                            self.display() 
                    elif rows == 0: # bord supérieur
                        if self.game.levelboard[rows+1][cols] in self.game.zones_coloriees\
                           or self.game.levelboard[rows][cols+1] in self.game.zones_coloriees\
                           or self.game.levelboard[rows][cols-1] in self.game.zones_coloriees:
                            ImageDraw.floodfill(self.board,coord_pix, self.colors[self.__count%4])
                            self.boardtk.paste(self.board)
                            self.game.scores(cols,rows,self.__count%4)
                            self.__count +=1
                            self.display()   
                    elif rows == 10: # bord inférieur
                        if self.game.levelboard[rows-1][cols] in self.game.zones_coloriees\
                           or self.game.levelboard[rows][cols+1] in self.game.zones_coloriees\
                           or self.game.levelboard[rows][cols-1] in self.game.zones_coloriees:
                            ImageDraw.floodfill(self.board,coord_pix, self.colors[self.__count%4])
                            self.boardtk.paste(self.board)
                            self.game.scores(cols,rows,self.__count%4) 
                            self.__count +=1
                            self.display()   

        if self.__count == 24 : # Partie terminée
            self.exit()
            Game_over(self.player1,self.player2,self.game._score_p1,self.game._score_p2)

   # --------------------------------------------------------------------------
    def display(self) :
        """Display score for both player, relief changes when a player is leading"""
        self.score_p1['text'] = "R : " + str(self.game._scores[0][0]) + ' * ' +  str(self.game._scores[0][1]) \
            + "  B : " + str(self.game._scores[2][0]) + ' * ' + str(self.game._scores[2][1]) \
                + "  => " + str(self.game._score_p1)
        self.score_p2['text'] = "V : " + str(self.game._scores[1][0]) + ' * ' +  str(self.game._scores[1][1]) \
            + "  J : " + str(self.game._scores[3][0]) + ' * ' + str(self.game._scores[3][1]) \
                + "  => " + str(self.game._score_p2)

        
        if self.game._score_p1 > self.game._score_p2 :
            self.players_frame1['relief'] = 'solid'
            self.players_frame2['relief'] = 'ridge'
        elif self.game._score_p2 > self.game._score_p1 :
            self.players_frame1['relief'] = 'ridge'
            self.players_frame2['relief'] = 'solid'
        else :
            self.players_frame1['relief'] = 'ridge'
            self.players_frame2['relief'] = 'ridge'
       
    # -------------------------------------------------------------------------
class Game_over(Win) :
    """End of game, saving stats"""
  # ---------------------------------------------------------------------------
    def __init__(self, player1, player2, score_p1, score_p2):
        """creation of the main window and packing gadgets"""
        Win.__init__(self, title='Game Over', op=0)
        # différents textes qui vont s'afficher, selon vainqueur (ou match nul)
        if score_p1 > score_p2: winner = "And the winner is " + player1 + " !!" 
        elif score_p2 > score_p1 : winner = "And the winner is " + player2 + " !!"
        else : winner = "It's a draw !"
        final_scores = " %s : %s pts  |  %s : %s pts " % (player1,score_p1, player2, score_p2) 
  # ---------------------------------------------------------------------------      
        Label(self, text = winner , font = "Arial 22 bold", height=3, bg='Black', fg='#99FF00')
        Label(self, text = final_scores , font = "Arial 20", height=3, bg='Black', fg='White')
        Butframe = Frame(self, flow = 'E', op=2, bg='Black')
        Button (Butframe, text = 'REVENGE',       command= self.revenge,     relief='flat', fg= 'Black', bg='White')
        Button (Butframe, text = 'CLEAR HISTORY', command= self.clear,       relief='flat', fg= 'Black', bg='White')
        Button (Butframe, text = 'HELP',          command= HelpWin,          relief='flat', fg= 'Black', bg='White')
        Button (Butframe, text = 'EXIT GAME',     command= self.exit,        relief='flat', fg= 'White', bg='Red')
  # ---------------------------------------------------------------------------
        write_txt("past_games.txt", '%s : %s : %s   |   %s : %s  --> %s' \
            % (str(dt.replace(dt.now(),microsecond = 0))[:-3],player1,score_p1,player2,score_p2, winner), 0)
        self.loop()
  # ---------------------------------------------------------------------------
    def clear(self):
        """Nettoyer le fichier d'historique des parties"""
        open('past_games.txt','w')
  # ---------------------------------------------------------------------------    
    def revenge(self):
        """Callback function for the revenge button""" 
        self.exit()
        ComboColorGUI()
  # ---------------------------------------------------------------------------    
    def exit(self):
        """function for EXIT button"""
        self.exit()
# ==============================================================================
class HelpWin(Win):
    """Class For the help window"""
  # --------------------------------------------------------------------------
    def __init__(self):
        """creation of the main window and packing gadgets"""
        Win.__init__(self, title='HELP', op=2)
        notice = read_txt("AideComboColor.txt")
        Label(self, text = notice, font = "Arial 12 bold")
        self.loop()
  # ---------------------------------------------------------------------------

# ==============================================================================
if __name__ == '__main__':
  ComboColorGUI()
# ==============================================================================

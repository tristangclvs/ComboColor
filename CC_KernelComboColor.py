# ==============================================================================
"""ComboColor : Create the Combo Color game"""
# ==============================================================================
__author__  = "Tristan Gonçalves, Terry Bouchez"
__version__ = "3.0" # calcul des scores + stockage des zones coloriées        
__date__    = "02/01/2020"
# ------------------------------------------------------------------------------
from ezCLI import read_blk, testcode, grid, write_txt


zones = {'A':(1,0), 'B':(1,0),'C':(1,0),'D':(1,0),'E':(2,0),'F':(2,0),'G':(2,0),'H':(2,0),\
         'I':(3,0), 'J':(3,0),'K':(3,0),'L':(4,0),'M':(4,0), 'N':(-2,0), 'O':(-2,0),'P':(-2,0),\
         'Q':(-4,0),'R':(-4,0),'S':(-6,0),'T':(-6,0),'U':(0,2),'V':(0,2),'W':(0,3),'X':(0,3)}

class KernelComboColor(object):
    """kernel class for the ComboColor game"""
    # --------------------------------------------------------------------------
    def __init__(self, selected_level):
        """initialize 'self' with chosen board"""
        self.board = [[0 for col in range(11)] for row in range(11)]

        self.selected_level = selected_level
        self._scores=[ [0,1] for i in range (4)] # on démarre à 1 la partie multiplicatrice 
                                                 # pour pas multiplier par 0 si l'on ne clique 
                                                 # pas sur une des cases "fois X"
        self.open_level(selected_level)

        # prend la lettre correspondant à la case grise (le Z)
        self.zones_coloriees = 'Z' # self.levelboard[5][5]
                                                            
    # --------------------------------------------------------------------------
    def __repr__(self) :
        """return object representation for 'self' """
        return "%s(selected_level = %s)" % (type(self).__name__, self.selected_level)
    # --------------------------------------------------------------------------
    def __eq__(self, peer):
        """test equality between 'self' and 'peer'"""
        return repr(self) == repr(peer)
    # --------------------------------------------------------------------------
    def __str__(self):
        """return string representation for 'self'"""
        board = [[self.levelboard[row][col] for col in range(11)] for row in range(11)]
        return grid(board, size = 3) # convert board matrix to multi-line grid string
    # ----------------------------------------------------------------------------
    def open_level(self, selected_level):
        """ Open the selected level """
        assert isinstance(selected_level, str) and selected_level in 'ABCDEF', "Choose a letter in 'A B C D E F'"
        self.levelboard = read_blk(f'Boards/board{selected_level}.txt') #terrain de jeu avec les lettres.
    # --------------------------------------------------------------------------
    def scores(self,x,y, player) : 
        
        self.zones_coloriees += self.levelboard[y][x]

        # Addition tags additifs et soustractifs ==> A
        # Essayer de faire les additions si zones[...] est dans les lettres qui font des ajouts, et sinon ça fait dans multiplication
        if self.levelboard[y][x]  in 'ABCDEFGHIJKLMNOPQRST' : #si on clique sur une zone d'addition 
            self._scores[player][0] += zones[self.levelboard[y][x]][0]
            self._scores[player][1] = self._scores[player][1]
        # Addition tags multiplicatifs           ==> M
        elif self.levelboard[y][x]  in 'UVWX' : # zone de multiplication
            self._scores[player][0] = self._scores[player][0] 
            self._scores[player][1] += (zones[self.levelboard[y][x]][1]-1)
        
        # Joueur 1 = AR*MR*AB*MB  [produit des scores rouge et bleu]
        # --> Joueur 1 = player --> 0 & 2        
        self._score_p1 = self._scores[0][0]*self._scores[0][1]*self._scores[2][0]*self._scores[2][1]

        # Joueur 2 = AG*MG*AY*MY  [produit des scores vert et jaune]
        # --> Joueur 2 = player --> 1 & 3
        self._score_p2 = self._scores[1][0]*self._scores[1][1]*self._scores[3][0]*self._scores[3][1]




if __name__ == "__main__": # testcode for class 'Kernel2048'
  print('\n'.join(('─'*80, __doc__, '─'*80)))
  code = r'''
a = KernelComboColor('A')
a

str(a)

a.scores(1,2,0)  # case F joueur 1 Rouge (+2)
a.scores(10,3,1) # case L joueur 2 Vert  (+4)
a.scores(3,5,2)  # case D joueur 1 Bleu  (+1)
a.scores(6,0,3)  # case T joueur 2 Jaune (-6)
print (a._score_p1,a._score_p2)

b = KernelComboColor('B')
b

str(b)
a==b

'''; testcode(code)
# ==============================================================================

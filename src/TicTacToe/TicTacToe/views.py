from djangorestframework.views import View
import uuid

from django.http import HttpResponse
from djangorestframework.renderers import JSONRenderer

class JSONResponse(HttpResponse):
    """
        An HttpResponse that renders its content into JSON.

        Params:
        data - data payload to return

        Default HTTP code will be 200 unless another is specified in kwargs
    """
    def __init__(self, data={}, **kwargs):
        # None passed to JSONRenderer sets view property which we don't use
        content = ""
        if data:
            content = JSONRenderer(None).render(data)
        kwargs['content_type'] = 'application/json; charset=utf-8'
        super(JSONResponse, self).__init__(content, **kwargs)



class TicTacToeView(View):
    """
    Return a unique ID
    """
    def put(self, request):
        
        data = self.DATA
        
        player=data.get('player')
        self.board=data.get('board')
        self.board = self.board.lower()
        player = player.lower()
        
        print self.board
        print player
        
        # Player x is always first to start
        if player == 'x':
            enemy = 'o'
        if player == 'o':
            enemy = 'x'
        
        movenum = 0
        numX = self.board.count('x')
        numO = self.board.count('o')
        won = 0
        
        if len(self.board) < 9:
            return
        
        if player == 'x':
            movenum = numX + 1
        if player == 'o':
            movenum = numO + 1
            
        # Take center spot if it's available, else take corner
        if movenum == 1 or movenum == 2:
            if self.board[4] == '-':
                self.replace_str(4, player)
            else:
                self.replace_str(0, player)
            return JSONResponse(data={'self.board': self.board, 'won': won}, status=200)
        
        # If on 2nd move enemy didn't take a corner spot
        if movenum == 3 and self.board[4] == player and self.board[0]=='-' and self.board[2]=='-' and self.board[6]=='-' and self.board[8]=='-':
            if self.board[1] == enemy or self.board[7] == enemy:
                self.replace_str(3, player)
            elif self.board[3] == enemy or self.board[5] == enemy:
                self.replace_str(1, player)
            return JSONResponse(data={'self.board': self.board, 'won': won}, status=200)
                
            
        if self.make_move(player, player):
            won = 1
            return JSONResponse(data={'self.board': self.board, 'won': won}, status=200)
            
        if self.make_move(player, enemy):
            return JSONResponse(data={'self.board': self.board, 'won': won}, status=200)
        
        if self.board[4] == player:
            if self.board[0] == '-' and self.board[8] == '-':
                self.replace_str(0, player)
            elif self.board[2] == '-' and self.board[6] == '-':
                self.replace_str(2, player)
            elif self.board[1] == '-' and self.board[7] == '-':
                self.replace_str(1, player)
            elif self.board[3] == '-' and self.board[5] == '-':
                self.replace_str(3, player)
            return JSONResponse(data={'self.board': self.board, 'won': won}, status=200)

        #if move_num == 0 and corner not taken:
            
         #   take 1st non corner
         #   take 1st corner with 1 neighbor
            
        #if move_num == 1:
        #    take center
        #    take 1st attack with at least 1 neighbor  
        
        return result
    
    def make_move(self, player, enemy):
        res = False
        
        if self.board[0] == '-' and ((self.board[1]==enemy and self.board[2]==enemy) or (self.board[3]==enemy and self.board[6]==enemy) or (self.board[4]==enemy and self.board[8]==enemy)):
            self.replace_str(0, player)
            res = True
        elif self.board[1] == '-' and ((self.board[0]==enemy and self.board[2]==enemy) or (self.board[4]==enemy and self.board[7]==enemy)):
            self.replace_str(1, player)
            res = True
        elif self.board[2] == '-' and ((self.board[0]==enemy and self.board[1]==enemy) or (self.board[5]==enemy and self.board[8]==enemy) or (self.board[4]==enemy and self.board[6]==enemy)):
            self.replace_str(2, player)
            res = True
        elif self.board[3] == '-' and ((self.board[0]==enemy and self.board[6]==enemy) or (self.board[4]==enemy and self.board[5]==enemy)):
            self.replace_str(3, player)
            res = True
        elif self.board[4] == '-' and ((self.board[0]==enemy and self.board[8]==enemy) or (self.board[1]==enemy and self.board[7]==enemy) or (self.board[2]==enemy and self.board[6]==enemy)\
                                  (self.board[3]==enemy and self.board[5]==enemy)):
            self.replace_str(4, player)
            res = True
        elif self.board[5] == '-' and ((self.board[2]==enemy and self.board[8]==enemy) or (self.board[3]==enemy and self.board[4]==enemy)):
            self.replace_str(5, player)
            res = True
        elif self.board[6] == '-' and ((self.board[0]==enemy and self.board[3]==enemy) or (self.board[2]==enemy and self.board[4]==enemy) or (self.board[7]==enemy and self.board[8]==enemy)):
            self.replace_str(6, player)
            res = True
        elif self.board[7] == '-' and ((self.board[1]==enemy and self.board[4]==enemy) or (self.board[6]==enemy and self.board[8]==enemy)):
            self.replace_str(7, player)
            res = True
        elif self.board[8] == '-' and ((self.board[2]==enemy and self.board[5]==enemy) or (self.board[0]==enemy and self.board[4]==enemy) or (self.board[6]==enemy and self.board[7]==enemy)):
            self.replace_str(8, player)
            res = True
         
        return res
    
    def replace_str(self, pos, c):
        newstr = list(self.board)
        newstr[pos] = c
        self.board =  "".join(newstr)
        
        
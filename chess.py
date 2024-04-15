class Piece:
    def __init__(self, x_coord, y_coord, color):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.color = color
        self.captured = False
        
    def is_valid_move(self, gamestate, to_square_coord):
        return False
    
    def move(self, gamestate, to_square_coord):
        
        '''if self.color != gamestate.current_player.color:
            print("It's not your turn!")
            return False
        
        if not self.is_valid_move(gamestate, to_square_coord):
            print("That's not a valid chess move!")
            return False
        '''
        self.x_coord, self.y_coord = to_square_coord
        #return True
        
class EmptySquare:
    def __init__(self, square_color):
        self.square_color = square_color
        self.symbol = "■" if square_color == 'white' else "□"

    def __str__(self):
        return self.symbol

    def is_valid_move(self, chessboard, end):
        return False
    
    def move(self, gamestate, to_square_coord):
        raise ValueError("Can't move empty square")

class Pawn(Piece):
    def __init__(self, x_coord, y_coord, color):
        super().__init__(x_coord, y_coord, color)

        self.symbol = '♟︎' if self.color == 'white' else '♙'
        self.name = 'pawn'
        #self.promoted = False # if necessary
    
    def __str__(self):
        return self.symbol
    
    def move(self, gamestate, to_square_coord):
        self.x_coord, self.y_coord = to_square_coord
        if self.is_promotion_position():
            self.promote(gamestate)
            
    def is_valid_move(self, chessboard, end):
        
        x1, y1 = self.x_coord, self.y_coord
        x2, y2 = end
        dx = abs(x2 - x1)
        dy = y2 - y1

        # determine direction based on color
        direction = -1 if self.color == 'black' else 1

        
        # pawn can only move forward
        if dy * direction <= 0:
            return False


        
        # pawn can move two spaces on first move
        if dy == 2 * direction and x1 == x2 and y1 == 2.5 * (-direction) + 3.5:
            if not isinstance(chessboard.get_piece((x1, y1 + direction)), EmptySquare) or not isinstance(chessboard.get_piece((x2, y2)), EmptySquare):
                return False
            return True

        # pawn can move one space forward, or diagonally if capturing
        if dx == 0:
            if not isinstance(chessboard.get_piece((x2, y2)), EmptySquare):
                return False
            if not isinstance(chessboard.get_piece((x1, y1 + direction)), EmptySquare):
                return False
            if dy == direction:
                return True
            else:
                return False
        elif dx == 1 and dy == direction:
            if isinstance(chessboard.get_piece((x2, y2)), EmptySquare) or chessboard.get_piece((x2, y2)).color == self.color:
                return False
            return True
        else:
            return False
            
    def promote(self, gamestate):
        '''
        Want to display board with pawn on last rank before asking for promotion. That means print(game.chessboard) needs to occur before I print again with the promoted piece, however, needs to print with correct pawn position. 
        How to do this intelligently? Can call the print before I take the input, but is the pawn coords updated at this point? YES THEY ARE. That's when to call it, and then will be printed again after new piece added.
        Would only want to call promote() when a pawn is moved, and is_valid_move is triggered when a pawn moves. So will call it in there. However, promote requires game to be passed, and game is not passed in any other is_valid_move methods. Therefore will have to update each method to call game.
        Will have to have loop to tell player to enter valid piece to promote to if they enter something invalid.l would do that either in get_piece or in promote
        '''
        #if game.current_player == 0:
        #if self.y_coord == 7 * ((game.current_player + 1) % 2):
        new_piece = self.get_promotion_piece()
        gamestate.chessboard.pieces_list.remove(self)
        gamestate.chessboard.pieces_list.append(new_piece)
            #self.promoted = True # not sure if necessary
            
    def get_promotion_piece(self):
        # print(game.chessboard) #can't do this unfortunately
        new_piece_str = input("Select piece to promote to (e.g. queen): ")
        while True:
            if new_piece_str.lower() == 'queen':
                return Queen(self.x_coord, self.y_coord, self.color)
            elif new_piece_str.lower() == 'rook':
                return Rook(self.x_coord, self.y_coord, self.color)
            elif new_piece_str.lower() == 'knight':
                return Knight(self.x_coord, self.y_coord, self.color)
            elif new_piece_str.lower() == 'bishop':
                return Bishop(self.x_coord, self.y_coord, self.color)
            else:
                new_piece_str = input("Invalid piece to promote to! Select piece to promote to (e.g. queen): ")
        

    def is_promotion_position(self):
        return (self.color == 'white' and self.y_coord == 7) or \
               (self.color == 'black' and self.y_coord == 0)
        
class Knight(Piece):
    def __init__(self, x_coord, y_coord, color):
        super().__init__(x_coord, y_coord, color)
       
        self.symbol = '♞' if self.color == 'white' else '♘'
        self.name = 'knight'
        
    def __str__(self):
        return self.symbol
     
    def is_valid_move(self, gamestate, end):
        file_start, rank_start = self.x_coord, self.y_coord
        # files are x coords, ranks are y coords (files are vertical columns, ranks are horizontal rows)
        rank_end, file_end = end
        abs_file = abs(file_end - file_start)
        abs_rank = abs(rank_end - rank_start)
        if abs_file + abs_rank == 3 and abs_file != 0 and abs_rank != 0   and rank_end >= 0 and file_end >= 0 and rank_end <= 7 and file_end <= 7:
            # handles index out of range error (after tab)
            end_piece = gamestate.chessboard.board[rank_end][file_end]
            if isinstance(end_piece, EmptySquare) or end_piece.color != self.color:
                return True
        return False


class Bishop(Piece):
    def __init__(self, x_coord, y_coord, color):
        super().__init__(x_coord, y_coord, color)
       
        self.symbol = '♝' if self.color == 'white' else '♗'
        self.name = 'bishop'
        
    def __str__(self):
        return self.symbol
        
    def path_is_blocked(self, start, end, board_obj):
        # replace this with self.x_coord, self.y_coord
        dx = end[0] - start[0]
        dy = end[1] - start[1]

        # Check that the move is diagonal
        if abs(dx) != abs(dy):
            print("not a valid move for a bishop")
            return False  # Not a valid move for a bishop

        # Determine the direction of movement
        step_x = 1 if dx > 0 else -1
        step_y = 1 if dy > 0 else -1

        x, y = start[0] + step_x, start[1] + step_y
        while x != end[0] and y != end[1]:
            if not isinstance(board_obj.board[x][y], EmptySquare): #if board_obj.board[x][y] == 1:  # Check if the square is occupied
                return True  # The path is blocked
            x += step_x
            y += step_y

        return False  # The path is not blocked

    def is_valid_move(self, game, end):
        file_start, rank_start = self.x_coord, self.y_coord
        # files are x coords, ranks are y coords (files are vertical columns, ranks are horizontal rows)
        rank_end, file_end = end
        if abs(file_end - file_start) == abs(rank_end - rank_start):
            if not self.path_is_blocked((rank_start, file_start), end, game.chessboard):
                end_piece = game.chessboard.board[rank_end][file_end]
                if isinstance(end_piece, EmptySquare) or end_piece.color != self.color:
                    return True
        return False


class Rook(Piece):
    def __init__(self, x_coord, y_coord, color):
        super().__init__(x_coord, y_coord, color)
       
        self.symbol = '♜' if self.color == 'white' else '♖'
        self.name = 'rook'
         
    def __str__(self):
        return self.symbol
    
    def path_is_blocked(self, start, end, board_obj):
        dx = end[0] - start[0]
        dy = end[1] - start[1]

        # Check that the move is horizontal or vertical
        if dx != 0 and dy != 0:
            print("not a valid move for a rook")
            return False  # Not a valid move for a rook

        # Determine the direction of movement
        step_x = 0 if dx == 0 else (1 if dx > 0 else -1)
        step_y = 0 if dy == 0 else (1 if dy > 0 else -1)

        x, y = start[0] + step_x, start[1] + step_y
        while x != end[0] or y != end[1]:
            if not isinstance(board_obj.board[y][x], EmptySquare):  # Check if the square is occupied
                return True  # The path is blocked
            x += step_x
            y += step_y

        return False  # The path is not blocked

    
    def is_valid_move(self, gamestate, end):
        file_start, rank_start = self.x_coord, self.y_coord
        # files are x coords, ranks are y coords (files are vertical columns, ranks are horizontal rows)
        file_end, rank_end = end
        if file_start == file_end or rank_start == rank_end:
            if not self.path_is_blocked((rank_start, file_start), end, gamestate.chessboard):
                end_piece = gamestate.chessboard.board[rank_end][file_end]
                if isinstance(end_piece, EmptySquare) or end_piece.color != self.color:
                    return True
        return False


class Queen(Piece):
    def __init__(self, x_coord, y_coord, color):
        super().__init__(x_coord, y_coord, color)
       
        self.symbol = '♛' if color == 'white' else '♕'
        self.name = 'queen'
    
    def __str__(self):
        return self.symbol
    
    def path_is_blocked_diag(self, start, end, board_obj):
        # replace this with self.x_coord, self.y_coord
        dx = end[0] - start[0]
        dy = end[1] - start[1]

        # Check that the move is diagonal
        if abs(dx) != abs(dy):
            print("not a valid move for a bishop")#bug
            return False  # Not a valid move for a bishop

        # Determine the direction of movement
        step_x = 1 if dx > 0 else -1
        step_y = 1 if dy > 0 else -1

        x, y = start[0] + step_x, start[1] + step_y
        while x != end[0] and y != end[1]:
            if not isinstance(board_obj.board[x][y], EmptySquare): #if board_obj.board[x][y] == 1:  # Check if the square is occupied
                return True  # The path is blocked
            x += step_x
            y += step_y

        return False  # The path is not blocked
    
    def path_is_blocked_verthoriz(self, start, end, board_obj):
        dx = end[0] - start[0]
        dy = end[1] - start[1]

        # Check that the move is horizontal or vertical
        if dx != 0 and dy != 0:
            print("not a valid move for a rook") #bug: a queen?
            return False  # Not a valid move for a rook

        # Determine the direction of movement
        step_x = 0 if dx == 0 else (1 if dx > 0 else -1)
        step_y = 0 if dy == 0 else (1 if dy > 0 else -1)

        x, y = start[0] + step_x, start[1] + step_y
        while x != end[0] or y != end[1]:
            if not isinstance(board_obj.board[x][y], EmptySquare):  # Check if the square is occupied
                return True  # The path is blocked
            x += step_x
            y += step_y

        return False  # The path is not blocked

    def path_is_blocked(self, start, end, board_obj):
        dx = end[0] - start[0]
        dy = end[1] - start[1]

        # Check that the move is diagonal
        if abs(dx) == abs(dy):
            return self.path_is_blocked_diag(start, end, board_obj)
       
        # Check that the move is horizontal or vertical
        if dx == 0 or dy == 0:
            return self.path_is_blocked_verthoriz(start, end, board_obj)  # Not a valid move for a rook

    def is_valid_move(self, gamestate, end):
        file_start, rank_start = self.x_coord, self.y_coord
        # files are x coords, ranks are y coords (files are vertical columns, ranks are horizontal rows)
        file_end, rank_end = end
        if not self.path_is_blocked((rank_start, file_start), end, gamestate.chessboard):
            end_piece = gamestate.chessboard.board[rank_end][file_end]
            if isinstance(end_piece, EmptySquare) or end_piece.color != self.color:
                return True
        return False
    
class King(Piece):
    def __init__(self, x_coord, y_coord, color):
        super().__init__(x_coord, y_coord, color)
       
        self.symbol = '♚' if self.color == 'white' else '♔'
        self.name = 'king'
    
    def __str__(self):
        return self.symbol
    
    def is_valid_move(self, gamestate, end):
        x1, y1 = self.x_coord, self.y_coord
        #this has to be 'backwards'
        x2, y2 = end
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        dist = max(dx, dy)
        if dist > 1:
            return False
        if not isinstance(gamestate.get_piece(end), EmptySquare) and gamestate.get_piece(end).color == self.color:
            return False
        return True



class ChessBoard:
    def __init__(self) -> None:
        
        self.pieces_list = []
        self.setup_pieces_list()
        self.board = []
        self.empty_and_setup_board()
        self.update_pieces_to_coords()
    
    def __str__(self):
        board_str = ""
        for row in self.board:
            row_str = ""
            for square in row:
                #gather row
                
                row_str += square.symbol + " " #+ board_str
            #display rows in reverse
            board_str = row_str + "\n" + board_str
            #board_str += '\n'
        
        return "\n" + board_str
    
    
    def get_piece(self, square):
        '''
        sig: tuple --> Square/None
        returns piece based on coords by indexing self.board[]
        '''
        if 0 <= square[0] <= 7 and 0 <= square[1] <= 7:
            return self.board[square[1]][square[0]]
        else:
            return None
    
    def setup_pieces_list(self):
        '''
        sig: none->none
        procedure for creating pieces list at beginning of game
        '''
        #append each piece with coords to board list
        for col in range(8):
            self.pieces_list.append(Pawn(col, 1, 'white'))
            self.pieces_list.append(Pawn(col, 6, 'black'))

        self.pieces_list.append(Rook(0, 0, 'white'))
        self.pieces_list.append(Knight(1, 0, 'white'))
        self.pieces_list.append(Bishop(2 ,0, 'white'))
        self.pieces_list.append(Queen(3 ,0, 'white'))
        self.pieces_list.append(King(4, 0, 'white'))
        self.pieces_list.append(Bishop(5, 0, 'white'))
        self.pieces_list.append(Knight(6, 0, 'white'))
        self.pieces_list.append(Rook(7, 0, 'white'))

        self.pieces_list.append(Rook(0, 7, 'black'))
        self.pieces_list.append(Knight(1, 7, 'black'))
        self.pieces_list.append(Bishop(2, 7, 'black'))
        self.pieces_list.append(Queen(3, 7, 'black'))
        self.pieces_list.append(King(4, 7, 'black'))
        self.pieces_list.append(Bishop(5, 7, 'black'))
        self.pieces_list.append(Knight(6, 7, 'black'))
        self.pieces_list.append(Rook(7, 7, 'black'))
        
    def empty_and_setup_board(self):
        '''
        Could improve this by iterating over all pieces and see if the pieces in pieces_list matches where they are in in board, and if they were not there, then put them where they should be in board
        Would do this using the 'is' operator, to check if an object IS that same object (not is identical, IS) 
        '''
        #first empty the board
        self.board = []

        #append each piece with coords to board list        
        for i in range(8):
            row = []
            for j in range(8):
                if (i+j)%2 == 0:
                    row.append(EmptySquare('black'))
                else:
                    row.append(EmptySquare('white'))
            self.board.append(row)
        
        #self.board.append([[EmptySquare(color=((i+j)%2==0)) for i in range(8)] for j in range(8)])
        
        
    def update_pieces_to_coords(self):
        #update pieces to corresponding spot in board[]
        #if try to promote to king, game crashes
        for square in self.pieces_list:
            if not square.captured:
                #y coord is item in list, x coord is item in item in list
                self.board[square.y_coord][square.x_coord] = square
          
    def update_board(self):
        # this method is called in gamestate
        self.empty_and_setup_board()
        self.update_pieces_to_coords()      
      
    def display_board(self):
        # this method is not called as of now, instead using __str__
        """
        sig: none --> none
        displays board to terminal, with rank1 as last rank, newlines between each rank, and spaces between each tile to make it display as a square
        """
        
        tiles = ''

        for i in range(self.size):
            rank = self.board_str[i]
            tiles = rank + '\n' + tiles 
        spaced_tiles = ''
        for char in tiles:
            if char != '\n':
                spaced_tiles += char + ' '
            else: spaced_tiles += char
        return spaced_tiles
    
    def is_check_after_move(self, move, current_player):
        #not finished, would not call this here anyway
        chessboard_next_move = self #create copy of chessboard obj (is this correct?)
        chessboard_next_move.process_move(move, current_player)
        """UNIMPLEMENTED"""
        pass
        

class Move:
    #should handle conversion of str in chess notation to coords
    def __init__(self, move) -> None:
        self.move = move
        self.from_square, self.to_square = self.move.split()
        self.from_square_coord = self.chess_notation_to_coord(self.from_square)
        self.to_square_coord = self.chess_notation_to_coord(self.to_square)
        self.from_x, self.from_y = self.from_square_coord
        self.to_x, self.to_y = self.to_square_coord
            

    def split_move(self):
        self.from_square, self.to_square = self.move.split()
        
    
    def validate_move_format(self, move_half):
        possible_letter_moves = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        if len(move_half) != 2 or not move_half[0].isalpha() or not move_half[1].isdigit() or move_half[0] not in possible_letter_moves or int(move_half[1]) < 1 or int(move_half[1]) > 8:
            raise ValueError("Invalid move format")
    
    def chess_notation_to_coord(self, move_half):
        self.validate_move_format(move_half)
        
        file, rank = move_half[0], move_half[1]
        file = ord(file) - 97
        rank = int(rank) - 1
        
        return file, rank #file is the x coord, rank is the y coord

class Player:
    def __init__(self, color) -> None:
        self.color = color
        
class HumanPlayer(Player):
    def get_move(self, gamestate):
        # only put example move on first move, no longer necessary every time
        while True:
            try:
                move = Move(input(f"{self.color.title()} player's turn. Enter your move (e.g. 'e2 e4'): "))
                piece = gamestate.get_piece(move.from_square_coord)
                
                if isinstance(piece, EmptySquare):
                    print("You can't move a non-existant piece!")
                elif piece.color != self.color:
                    print("It's not your turn!")
                elif piece.is_valid_move(gamestate, move.to_square_coord):
                    return move #return the valid move
                else:
                    print("Invalid move!")
                    
            except ValueError:
                print("Invalid move format!") #check for the raised error in move
        
    
     
class AIPlayer(Player):
    def get_move(self, gamestate):
        # Temporarily have another user input for AI's move
        # only put example move on first move, no longer necessary every time
        while True:
            try:
                move = Move(input(f"{self.color.title()} player's turn. Enter your move (e.g. 'e2 e4'): "))
                piece = gamestate.get_piece(move.from_square_coord)
                
                if isinstance(piece, EmptySquare):
                    print("You can't move a non-existant piece!")
                elif piece.color != self.color:
                    print("It's not your turn!")
                elif piece.is_valid_move(gamestate, move.to_square_coord):
                    return move #return the valid move
                else:
                    print("Invalid move!")
                    
            except ValueError:
                print("Invalid move format!") #check for the raised error in move
        
        
class GameState:
    def __init__(self, chessboard, current_player, castling_rights, en_passant_target):
        self.chessboard = chessboard # ChessBoard()
        #self.pieces = pieces
        #self.players = players # [HumanPlayer('white'), AIPlayer('black')]
        #self.current_player_index = current_player_index # 0. index of the current player in self.players: 0 for white, 1 for black
        self.current_player = current_player
        self.castling_rights = castling_rights # {'white': ['e1 c1', 'e1 g1'], 'black': ['e8 c8', 'e8 g8']} //might have to set these as coordinates, depending on how moves are represented in is_valid_move 
        self.en_passant_target = en_passant_target # None, or 'c3'

    '''def play(self):
        
        while not self.is_over():
            print(self.chessboard)
            
            player = self.players[self.current_player]
            player.make_move(self)
            self.current_player = (self.current_player + 1) % 2  # switch to the other player  
    '''
    
    def get_piece(self, square_coord):
        from_x, from_y = square_coord
        return self.chessboard.board[from_y][from_x]
    
    def make_move(self, move):
        self.chessboard.board[move.from_y][move.from_x].move(self, move.to_square_coord)
        self.chessboard.update_board()
    
    
    def is_game_over(self):
        # Check if game is over
        return False

class Node:
    pass

class MinimaxTree:
    """UNIMPLEMENTED"""
    def __init__(self, tree, present) -> None:
        
        self.tree = tree
        self.present = present

    def find_best_game(self):
        pass
    
    def find_best_move(self):
        '''
        how to find best move, that would be 
        '''
        pass
   
   
class ChessGame:
    def __init__(self) -> None:
        self.players = [HumanPlayer('white'), AIPlayer('black')]
        self.current_state = GameState(ChessBoard(), self.players[0], {'white': ['e1 c1', 'e1 g1'], 'black': ['e8 c8', 'e8 g8']}, None)
        #later, update this to allow human player to choose which color they want to play

        
    def play(self):
        while not self.current_state.is_game_over():
            print(self.current_state.chessboard)
            
            #player = self.players[self.current_state.current_player]
            move = self.current_state.current_player.get_move(self.current_state)
            self.current_state.make_move(move)
            self.current_state.current_player = self.players[1] if self.current_state.current_player.color == 'white' else self.players[0] # switch to the other player  
 
game = ChessGame()
game.play()
 

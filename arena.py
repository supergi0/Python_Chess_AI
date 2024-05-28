import chess
import Chess_Agent
import chess.svg
from time import sleep
import time
import cairosvg
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

board = chess.Board()
white = Chess_Agent.group1("white")
black = Chess_Agent.group1("black")
winner = "tie"

gameOver = False
iterations = 0
turn =-1
svgcontent = chess.svg.board(board, size=350)
img_png = cairosvg.svg2png(svgcontent)
img = Image.open(BytesIO(img_png))
plt.imshow(img)
plt.draw()
plt.pause(0.001)
plt.draw()
plt.pause(0.001)
plt.draw()
plt.pause(0.001)
sleep(1)

white_time = 0
black_time = 0

while not gameOver and (iterations<10000):
    if(turn<0):
        #logic for white move
        print('Whites move')
        start_time = time.time()
        move = white.makemove(board)
        end_time = time.time()
        white_time += end_time - start_time
        if chess.Move.from_uci(move) in board.legal_moves:
            uci_move = chess.Move.from_uci(move)
            board.push(uci_move)
        else:
            winner = "black"
            gameOver = True
        
        if board.is_checkmate():
            winner = "white"
            gameOver = True
            
        if board.is_stalemate():
            winner = "tie"
            gameOver = True
            
        svgcontent = chess.svg.board(board, size=350)
        img_png = cairosvg.svg2png(svgcontent)
        img = Image.open(BytesIO(img_png))
        plt.imshow(img)
        plt.draw()
        plt.pause(0.001)
            
    else:
        #logic for black move
        print('Blacks move')
        start_time = time.time()
        move = black.makemove(board)
        end_time = time.time()
        black_time += end_time - start_time
        if chess.Move.from_uci(move) in board.legal_moves:
            uci_move = chess.Move.from_uci(move)
            board.push(uci_move)
        else:
            winner = "white"
            gameOver = True
            
        if board.is_checkmate():
            winner = "black"
            gameOver = True
            
        if board.is_stalemate():
            winner = "tie"
            gameOver = True
            
        svgcontent = chess.svg.board(board, size=350)
        img_png = cairosvg.svg2png(svgcontent)
        img = Image.open(BytesIO(img_png))
        plt.imshow(img)
        plt.draw()
        plt.pause(0.001)
        
    iterations = iterations+1
    turn = turn*-1
    sleep(1)
    
print("And the winner is .... "+winner)
print(f"Total time taken by white bot: {white_time} seconds")
print(f"Total time taken by black bot: {black_time} seconds")    
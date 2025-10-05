from flask import Flask,render_template,redirect
from flask_socketio import SocketIO
import numpy as np

app = Flask(__name__)
socketio = SocketIO(app)

import time
class Board:
    def __init__(self,height=6,width=7):
        self.height = height
        self.width = width
        self.board = self.createMatrix()
        self.valid = [0 for i in range(self.width)]

    def createMatrix(self):
        return [[0 for i in range(self.width)] for j in range(self.height)]
    
    def disp(self):
        for i in self.board:
            for j in i:
                if j=="X":
                    print("🟢",end="")
                elif j=="O":
                    print("🔴",end="")
                else:
                    print("⚪",end="")
            print()
        for i in range(self.width):
            print(i+1,end=" ")
        print("\n")

    def insert(self,column,data):
        if self.valid[column]==self.height:
            return False
        self.board[self.height-self.valid[column]-1][column]=data
        self.valid[column]+=1
        return True
    
    def delete(self,column):
        if self.valid[column]==0:
            return False
        self.valid[column]-=1
        self.board[self.height-self.valid[column]-1][column]=0
        return True
    
    def heurSupport(self,column,p=False):
        num = {"X":0,"O":0,0:0}
        pos = {0:0,1:0,2:0,3:0,4:0}
        if column<0 or column>=self.width:
            return pos
        x = [[-1,-2,-3],[0,0,0],[1,2,3],[1,2,3],[1,2,3],[0,0,0],[-1,-2,-3]]
        y = [[-1,-2,-3],[-1,-2,-3],[-1,-2,-3],[0,0,0],[1,2,3],[1,2,3],[1,2,3]]
        index = self.height - self.valid[column]
        temp = self.board[index][column]
        seven = [0 for i in range(7)]
        for i in range(7):
            num = {"X":0,"O":0,0:0}
            num[temp]=1
            flag = True
            for j in range(3):
                y1 = column + y[i][j]
                x1 = index + x[i][j]
                if x1>=0 and y1>=0 and x1<self.height and y1<self.width:
                    if self.board[x1][y1]==temp or self.board[x1][y1]==0:
                        num[self.board[x1][y1]]+=1
                    else:
                        break
                else:
                    break
            seven[i]=num[temp]
        xtemp = [0,1,2]
        for i in range(3):
            if seven[xtemp[i]]+seven[xtemp[i]+4]-1>=3:
                if seven[xtemp[i]]+seven[xtemp[i]+4]-1>3:
                    pos[4]+=1
                else:
                    pos[3]+=1
        if p:
            print(seven)
        return pos
    
    def score(self,pos):
        penality = 0
        for i in range(2,5):
            penality += pos[i]*(10**i)
        return penality

    def heuristic(self,column):
        ans = self.score(self.heurSupport(column))
        index = self.height - self.valid[column]
        temp = self.board[index][column]
        self.delete(column)
        if temp=="X":
            self.insert(column,"O")
            heur = self.heurSupport(column)
            for i in range(4):
                heur[i] = heur[i+1]
            heur[4]=0
            ans = ans + 2*self.score(self.heurSupport(column))
        else:
            self.insert(column,"X")
            heur = self.heurSupport(column)
            for i in range(4):
                heur[i] = heur[i+1]
            heur[4]=0
            ans = -1*(ans + 2*self.score(self.heurSupport(column)))
        self.delete(column)
        self.insert(column,temp)
        return ans

    def winloss(self,column,p=False):
        num = {"X":0,"O":0,0:0}
        pos = {0:0,1:0,2:0,3:0,4:0}
        if column<0 or column>=self.width:
            return pos
        x = [[-1,-2,-3],[0,0,0],[1,2,3],[1,2,3],[1,2,3],[0,0,0],[-1,-2,-3]]
        y = [[-1,-2,-3],[-1,-2,-3],[-1,-2,-3],[0,0,0],[1,2,3],[1,2,3],[1,2,3]]
        index = self.height - self.valid[column]
        temp = self.board[index][column]
        
        for i in range(7):
            num = {"X":0,"O":0,0:0}
            num[temp]=1
            flag = True
            for j in range(3):
                y1 = column + y[i][j]
                x1 = index + x[i][j]
                if x1>=0 and y1>=0 and x1<self.height and y1<self.width:
                    if (self.board[x1][y1]==temp):
                        num[self.board[x1][y1]]+=1
                    else:
                        flag=False
                        break
                else:
                    break
            if flag:
                pos[num[temp]]+=1
        seven = [0 for i in range(7)]
        for i in range(7):
            num = {"X":0,"O":0,0:0}
            num[temp]=1
            flag = True
            for j in range(3):
                y1 = column + y[i][j]
                x1 = index + x[i][j]
                if x1>=0 and y1>=0 and x1<self.height and y1<self.width:
                    if self.board[x1][y1]==temp:
                        num[self.board[x1][y1]]+=1
                    else:
                        break
                else:
                    break
            seven[i]=num[temp]
        xtemp = [0,1,2]
        for i in range(3):
            if seven[xtemp[i]]+seven[xtemp[i]+4]-1>=3:
                if seven[xtemp[i]]+seven[xtemp[i]+4]-1>3:
                    pos[4]+=1
                else:
                    pos[3]+=1
        if p:
            print(seven)
        return pos
    def reset(self):
        self.board = self.createMatrix()
        self.valid = [0 for i in range(self.width)]
    
class Connect4:
    board = None
    player = None
    def __init__(self):
        self.board = Board()
        self.player = True

    def next_move_alpha_beta(self,player,cur_depth,max_depth,column=0,alpha=float('-inf'),beta=float('inf'),p=False):
        if cur_depth!=0:
            score = self.board.winloss(column)
            if score[4]>0 and (not player):
                return 10**5 + max_depth - cur_depth,column
            if score[4]>0 and player:
                return -(10**5 + max_depth - cur_depth),column
        if cur_depth == max_depth:
            return self.board.heuristic(column),column

        if player:
            ma = float('-inf')
            index = -1
            hello = ["N" for i in range(7)]
            for i in [3,2,4,1,5,0,6]:
                if self.board.insert(i,"X"):
                    temp,j = self.next_move_alpha_beta(False,cur_depth+1,max_depth,i,alpha,beta)
                    hello[i]=temp + max_depth - cur_depth
                    self.board.delete(i)
                    if j!=-1:
                        if temp > ma:
                            ma = temp
                            index = i
                        alpha = max(temp,alpha)
                        if alpha >= beta:
                            break
            if hello==["N" for i in range(7)]:
                return 0,column
            if p:
                print(hello)
            return ma + max_depth - cur_depth,index
        else:
            mi = float('inf')
            index = -1
            hello = ["N" for i in range(7)]
            for i in [3,2,4,1,5,0,6]:
                if self.board.insert(i,"O"):
                    temp,j = self.next_move_alpha_beta(True,cur_depth+1,max_depth,i,alpha,beta)
                    hello[i]=temp - max_depth + cur_depth,j
                    self.board.delete(i)
                    if j!=-1:
                        if temp < mi:
                            mi = temp
                            index = i
                        beta = min(temp,beta)
                        if alpha >= beta:
                            break
            if hello==["N" for i in range(7)]:
                return 0,column
            if p:
                print(hello)
            return mi - max_depth + cur_depth,index
            

    def start_game(self):
        print("Game Started")
        count = 42
        self.board.disp()
        while count!=0:
            count-=1
            move = -1
            if self.__player:
                self.__player = False
                while True:
                    try:
                        temp = int(input("Enter a value from 1-7: "))
                        if temp<1 or temp>7:
                            continue
                        if not self.board.insert(temp-1,"X"):
                            continue
                        break
                    except KeyboardInterrupt:
                        exit()
                    except:
                        continue
                
                move = temp-1
            else:
                self.__player = True
                time1 = time.time()
                val,index = self.next_move_alpha_beta(False,0,6,p=True)
                print(f"Time taken by AI: {round(time.time()-time1,3)}s")
                self.board.insert(index,"O")
                move = index
                print(f"Index: {index} Value: {val}")
            final = self.board.winloss(move,True)
            print("Current move:",move+1)
            self.board.disp()
            if final[4]>0 and (not self.__player):
                print("🟢 won")
                break
            elif final[4]>0 and self.__player:
                print("🔴 won")
                break
        if count==0:
            print("Draw......Noice")
        print("Game Ended!!!")

#### Start of CNN

# Load weights for NumPy forward pass
weights_data = np.load("/home/sachcith/Documents/Github/Connect-4_Game/cnn_weights.npz", allow_pickle=True)
weights = {
    "conv1_w": weights_data[weights_data.files[0]],       # conv2d
    "conv1_b": weights_data[weights_data.files[1]],
    "conv2_w": weights_data[weights_data.files[2]],     # conv2d_1
    "conv2_b": weights_data[weights_data.files[3]],
    "dense1_w": weights_data[weights_data.files[4]],       # dense
    "dense1_b": weights_data[weights_data.files[5]],
    "dense2_w": weights_data[weights_data.files[6]],     # dense_1
    "dense2_b": weights_data[weights_data.files[7]],
    "dense3_w": weights_data[weights_data.files[8]],     # dense_2
    "dense3_b": weights_data[weights_data.files[9]]
}

# --- NumPy forward pass functions ---
def relu(x):
    return np.maximum(0, x)

def softmax(x):
    e = np.exp(x - np.max(x))
    return e / np.sum(e, axis=-1, keepdims=True)

def conv2d_numpy(x, weight, bias, stride=1, padding='same'):
    # x: (H,W,C_in), weight: (kH,kW,C_in,C_out), bias: (C_out,)
    H, W, C_in = x.shape
    kH, kW, _, C_out = weight.shape
    if padding == 'same':
        pad_h = (kH - 1) // 2
        pad_w = (kW - 1) // 2
        x_padded = np.pad(x, ((pad_h,pad_h),(pad_w,pad_w),(0,0)), mode='constant')
    else:
        x_padded = x
    H_out = (x_padded.shape[0] - kH)//stride + 1
    W_out = (x_padded.shape[1] - kW)//stride + 1
    out = np.zeros((H_out, W_out, C_out))
    for i in range(H_out):
        for j in range(W_out):
            for c in range(C_out):
                region = x_padded[i:i+kH, j:j+kW, :]
                out[i,j,c] = np.sum(region * weight[:,:,:,c]) + bias[c]
    return out

def maxpool2d_numpy(x, pool_size=2, stride=2):
    H, W, C = x.shape
    H_out = (H - pool_size)//stride + 1
    W_out = (W - pool_size)//stride + 1
    out = np.zeros((H_out, W_out, C))
    for i in range(H_out):
        for j in range(W_out):
            region = x[i*stride:i*stride+pool_size, j*stride:j*stride+pool_size, :]
            out[i,j,:] = np.max(region, axis=(0,1))
    return out

def forward_pass(board, weights):
    x = board.astype(np.float32)  # (6,7,1)

    # Conv1 + ReLU + MaxPool
    out1 = conv2d_numpy(x, weights['conv1_w'], weights['conv1_b'])
    out1 = relu(out1)
    out1_pool = maxpool2d_numpy(out1, pool_size=2, stride=2)  # (3,3,64)

    # Conv2 + ReLU + MaxPool
    out2 = conv2d_numpy(out1_pool, weights['conv2_w'], weights['conv2_b'])
    out2 = relu(out2)
    out2_pool = maxpool2d_numpy(out2, pool_size=2, stride=2)  # (1,1,128)

    # Flatten
    flat = out2_pool.flatten().reshape(1, -1)  # (1,128)

    # Dense layers
    dense1 = relu(flat @ weights['dense1_w'] + weights['dense1_b'])  # (1,256)
    dense2 = relu(dense1 @ weights['dense2_w'] + weights['dense2_b'])  # (1,128)
    logits = dense2 @ weights['dense3_w'] + weights['dense3_b']  # (1,3)
    
    probs = softmax(logits)
    return probs[0]

x=7
y=6

game = [[0 for i in range(x)]for i in range(y)]

def printgame():
    for i in game:
        for j in i:
            print(j,end="  ")
        print()

def drop_piece(a,p):
    for i in range(y):
        if game[y-i-1][p-1]==0 :
            game[y-i-1][p-1] = a
        
            if check_win(p-1, y-i-1, a):
                print(f"Player {a} wins!")
                return True
                
            return False
            
    print(f"Column {p} full, try again")
    return False

def check_win(col, row, player):
    directions = [
        (0, 1),
        (1, 0),
        (1, 1),
        (1, -1)
    ]
    for dr, dc in directions:
        count = 1
        r, c = row + dr, col + dc
        while 0 <= r < y and 0 <= c < x and game[r][c] == player:
            count += 1
            r += dr
            c += dc
        r, c = row - dr, col - dc
        while 0 <= r < y and 0 <= c < x and game[r][c] == player:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
            
    return False
    
def is_board_full():
    return all(game[0][col] != 0 for col in range(x))

def play_game():
    current_player = 1
    print("Connect 4 Game!")
    print("Players are 1 and 2")
    printgame()
    
    while True:
        print(f"\nPlayer {current_player}'s turn:")
        
        if drop_piece(current_player):
            printgame()
            break
            
        if is_board_full():
            print("Board is full! It's a tie!")
            printgame()
            break
            
        printgame()
        current_player = 2 if current_player == 1 else 1

def ai_move(player):
    best_score = -1
    best_col = None
    for col in range(x):
        # Check if column is valid
        if game[0][col] != 0:
            continue
        # Copy board and simulate move
        temp_board = [row.copy() for row in game]
        for row in range(y-1, -1, -1):
            if temp_board[row][col] == 0:
                temp_board[row][col] = player
                break
        # Convert to numpy array and reshape for CNN
        input_board = np.array(temp_board).reshape(6,7,1)
        pred = forward_pass(input_board,weights)
        win_prob = pred[2]  # probability of "win"
        if win_prob > best_score:
            best_score = win_prob
            best_col = col
    # Drop piece in best column
    for row in range(y-1, -1, -1):
        if game[row][best_col] == 0:
            game[row][best_col] = player
            return best_col

def play_game_ai():
    current_player = 1  # Human starts
    print("Connect 4 Game!")
    print("Player 1 = Human, Player 2 = AI")
    printgame()
    
    while True:
        print(f"\nPlayer {current_player}'s turn:")
        
        if current_player == 1:
            if drop_piece(current_player):  # Human move
                printgame()
                print("Human wins!")
                break
        else:
            if ai_move(current_player):  # AI move ------------------------------
                printgame()
                print("AI wins!")
                break
                
        if is_board_full():
            print("Board is full! It's a tie!")
            printgame()
            break
        
        printgame()
        current_player = 2 if current_player == 1 else 1

def reset_game():
    global game
    game = [[0 for _ in range(x)] for _ in range(y)]

#### End of CNN




board = Connect4()
count = 42
difficulty = "Hard"
current_player = 1 

@app.route('/')
def home():
    return render_template('index.html',board=board.board.board)

@socketio.on("move")
def move(data):
    col = int(data["col"])
    print(f"Column Clicked: {col}")
    if board.board.insert(col,"X")==False:
        socketio.emit("debug",{"debug": "Column Already Full!!"})
        socketio.emit("allow",{})
    else:
        global count,difficulty,current_player
        drop_piece(current_player,col+1)
        current_player = 2 if current_player == 1 else 1
        count-=1
        socketio.emit("debug",{"debug": "Okay!!"})
        temp = board.board.winloss(col)
        socketio.emit("player",{"cell":col+7*(6-board.board.valid[col])})
        val,index=0,0
        if difficulty=="hard":
            if temp[4]>0:
                socketio.emit("winloss",{"output":"🔴 Won"})
                return
            val,index=0,0
            if count<17:
                val,index = board.next_move_alpha_beta(False,0,max(count,2),p=True)
            else:
                val,index = board.next_move_alpha_beta(False,0,6,p=True)
        elif difficulty=="medium":
            if temp[4]>0:
                socketio.emit("winloss",{"output":"🔴 Won"})
                return
            val,index=0,0
            if count<5:
                val,index = board.next_move_alpha_beta(False,0,max(count,2),p=True)
            else:
                val,index = board.next_move_alpha_beta(False,0,3,p=True)
        else:
            if temp[4]>0:
                socketio.emit("winloss",{"output":"🔴 Won"})
                return
            index = ai_move(current_player)
            current_player = 2 if current_player == 1 else 1
        board.board.insert(index,"O")
        count-=1
        move = index
        print(f"Played by AI Index: {index} Value: {val}")
        socketio.emit("ai",{"cell":move+7*(6-board.board.valid[move])})
        temp = board.board.winloss(move)
        if temp[4]>0:
            socketio.emit("winloss",{"output":"🟢 Won"})
            return
        print(f"Count: {count}")
        if count==0:
            print("It is a Draw")
            socketio.emit("winloss",{"output":"Draw!!"})
            return
        socketio.emit("allow",{})

@app.route('/resetThing',methods=["GET","POST"])
def reset1():
    print("Inside reset")
    board.board.reset()
    print("Board Resetted...................")
    global count
    count = 42
    reset_game()
    return redirect('/')

@app.route('/easy',methods=["GET","POST"])
def easy():
    global difficulty
    difficulty = "easy"
    print(difficulty)
    return reset1()

@app.route('/hard',methods=["GET","POST"])
def hard():
    global difficulty
    difficulty = "hard"
    print(difficulty)
    return reset1()

@app.route('/medium',methods=["GET","POST"])
def medium():
    global difficulty
    difficulty = "medium"
    print(difficulty)
    return reset1()




'''
@socketio.on("reset")
def reset(data):
    print("Inside reset")
    if data["reset"]==1:
        board.board.reset()
        print("Board Resetted...................")
        return redirect('/')
'''

if __name__=="__main__":
    app.run(debug=True)
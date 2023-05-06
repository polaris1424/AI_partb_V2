# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent
import copy
import random
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir
from referee.game.board import Board
from typing import Optional
from agent.node import Node


# This is the entry point for your game playing agent. Currently the agent
# simply spawns a token at the centre of the board if playing as RED, and
# spreads a token at the centre of the board if playing as BLUE. This is
# intended to serve as an example of how to use the referee API -- obviously
# this is not a valid strategy for actually playing the game!

class Agent:
    def __init__(self, color: PlayerColor, **referee: dict):
        """
        Initialise the agent.
        """
        self._color = color
        match color:
            case PlayerColor.RED:
                print("Testing: I am playing as red")
            case PlayerColor.BLUE:
                print("Testing: I am playing as blue")
        self.board = Board() #空棋盘初始化
        #print(my_board.render())

        
    def action(self, **referee: dict) -> Action:
        """
        Return the next action to take.
        """
        #if self.board._state is none, spawn at the center
        match self._color:
            case PlayerColor.RED:           
                if self.board._state == {}: #empty board
                    print("!!!!!!!!!!!!空")
                    return SpawnAction(HexPos(3, 3))
                else:
                    #use MCTS to get the best action
                    best_action = self.mcts(self.board)
                    return best_action

            case PlayerColor.BLUE:
                #use MCTS to get the best action
                if self.board._state == {}: #empty board
                    #print("!!!!!!!!!!!!空")
                    return SpawnAction(HexPos(3, 3))
                else:
                    #use MCTS to get the best action
                    best_action = self.mcts(self.board)
                    return best_action
        #print("目前是self._color:",self._color)
        #print("best_action:",best_action)

  
    def mcts(self, board) -> Action:
        num_iterations = 100#，50可以100不可以
        print("mcts开始***********************")
         
        root = Node(state=board) #初始化根节点,传入当前棋盘状态")
        #legal_list =[]  
        #root_action_list = self.get_action_list(root.state,self._color)
        #action_num = len(root_action_list) 
        while(num_iterations):                 
            print("num_iterations:",num_iterations)
           # print("新的iteration 开始了，root的棋盘状态，应该只有一个棋子")
            #print(board.render())
            legal_list =[]
            #legal_list = self.get_action_list(root.state,self._color)
            #print("当前棋盘状态下，可供选择的action有,action_list会减少：",legal_list)
            # Selection
            #if(num_iterations<=9):
                #print("selecton前的slef_color 是：",self._color)
            select_node, legal_list, colour = self.selection(root, self._color) #action_num是当前root的action数量,用于判断是否fully expanded
            #print("当前棋盘状态下，可供选择的action有,legal_list会减少：",legal_list)
            #print("get_action_list找的颜色", colour)
            #print("==================seletion 完成==================")
            # expansion, spread random_node的六个方向
            # *6 spread, + empty cell spawn, random返回一个下一步随机的一个新的点
            #print("--------slect_node.state--------------``````````````: \n", select_node.state.render())
            if(num_iterations<=60):
                print("--------slect_node.state--------------``````````````: \n", select_node.state.render())

            random_node = self.expansion(select_node,legal_list, colour)  #update legal_list,remove random_node
            #print("==================expansion 完成==================")
            if(num_iterations<=60):
               print("==================expansion 完成，expansion后的状态==================")
              # print(random_node.state.render())
            
            # Simulation
            socre = self.simulation(random_node,num_iterations)
            if(num_iterations<=60):
               print("==================simulation 完成==================")
            #print("==================esimulation 完成==================")
            #print(random_node.state._state)
            # Backpropagation
            self.backpropagation(random_node, socre, self._color)
            


           # print("==================回溯 完成==================")
  
            num_iterations -= 1 #递减
            #legal_list.remove(random_action) #删除iteration里已经走过的action
        
        best_child = root.best_child() #获取child里ucb1值最高的
        #print("返回的beast action是: ",best_child.action)
        return best_child.action

  
    def selection(self, node: Node, colour:PlayerColor) -> Optional[Node]:
        #print("selection函数里的Node的棋盘状态")
        #print(node.state.render())
        legal_list = self.get_action_list(node.state,colour)
        #print("get_action_list找的颜色", colour)
        num = len(legal_list)
        #print("num:",num)

        if node.is_terminal():
           # print("当前选中的是终止节点》》》》》》")
           # print("select node 输出棋盘状态")
            #print(node.state.render())
            #从legal_list中删除每个child的action
            for child in node.children:
                if child.action in legal_list:
                    legal_list.remove(child.action)
            return node,legal_list,colour   
        if node.is_leaf():
           # print("走这，当前节点是叶子节点》》》》》》")
            #print("select node 输出棋盘状态")
            #print(node.state.render())
            for child in node.children:
                if child.action in legal_list:
                    legal_list.remove(child.action)
            return node,legal_list,colour
           
        #fully expanded
        if len(node.children) != num:  #如果当前节点的所有子节点还没被扩展过了
            #print("还没fully expanded ")
            #print(node.state.render())
            for child in node.children:
                if child.action in legal_list:
                    legal_list.remove(child.action)
            return node,legal_list,colour
            s
        # 否则，选择最佳子节点进行扩展
        #print("已经root 的childe全部显现了，选择下一个好child的child")
        #print(node.best_child.state.render())
        #change color
        match self._color:
            case PlayerColor.RED:
                colour = PlayerColor.BLUE
            case PlayerColor.BLUE:
                colour = PlayerColor.RED
        return self.selection(node.best_child(),colour)

    def expansion(self, node: Node, legal_list:list[Action], colour:PlayerColor) -> Node:
         
        #store all possible actions including spawn and spread
        #print("查看selction选中的，传入expansion的棋盘状态应该是root的@@@@@@@@@@@@@@@@@@@@@@@@")
        #print(node.state.render())
        match self._color:
        #match node.action_colour:
            case PlayerColor.RED:
                #action_list = self.get_action_list(node.state,self._color) #获取所有可能的action
                random_action = random.choice(legal_list)#随机选择一个action
                new_state = copy.deepcopy(node.state) #deepcopy当前棋盘状态    
                if(node.state._total_power <= 48):
                    new_state.apply_action(random_action)#在新棋盘上执行这个action           
                
               # print("复制棋盘棋盘供expansion apply action")
              #  print(new_state.render())          
                new_node = Node(parent=node, state=new_state, action=random_action, action_colour=colour)#新建一个node，加入到children里
                #print("子节点的棋盘状态!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", new_node.state.render())
              
                #print("选择的随机动作动作: ", random_action)
                node.children.append(new_node)#将新建的node加入到children里
            
                #deepcopy new_node
                copy_node = copy.deepcopy(new_node)#deepcopy新建的node，供  simulation使用
                return copy_node#返回新建的node
            case PlayerColor.BLUE:
                #action_list = self.get_action_list(node.state,self._color)
                #if action_list == []:
                #    print("空list!~~~~~~~~~~~~~~~~~~~~~")
                #print("action_list:", action_list)
                random_action = random.choice(legal_list)
                new_state = copy.deepcopy(node.state)        
                if(node.state._total_power <= 48):
                    new_state.apply_action(random_action)#在新棋盘上执行这个action         
               # print("复制棋盘棋盘供expansion apply action")
               # print(new_state.render())   
                     
                new_node = Node(parent=node, state=new_state, action=random_action, action_colour=colour) #新建一个node，加入到children里
               #print("子节点的棋盘状态!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", new_node.state.render())
                 
                #print("选择的随机动作动作: ", random_action)
                node.children.append(new_node)
            
                #deepcopy new_node
                copy_node = copy.deepcopy(new_node) #deepcopy新建的node，供  simulation使用  
                return copy_node   #返回新建的node

    def get_action_list(self, board: Board, colour:PlayerColor) -> list:
        #print("执行action_list函数， 函数里的颜色是：", colour)
        #board.render()
        
        
        """
        if colour == PlayerColor.RED:
            colour = PlayerColor.BLUE
            print("111111")
        else:
            colour = PlayerColor.RED
        
            print("22222") 
        """
        #print("颜色变成：", colour)  
        same_colour_list = [] #存放同色的棋子
        same_colour_list = self.take_same_colour(board, colour)
        spread_action_list = self.full_spread(same_colour_list)
        empty_cell_list = self.take_empty_cell(board)     
        #print("emoty_cell_list: ", empty_cell_list)
        spawn_action_list = self.fully_spawn(empty_cell_list)           
        
        action_list = spread_action_list + spawn_action_list 
        #print("action_list: ", action_list)
        #空一行
        #print()

        return action_list

    def simulation(self, node: Node, num_iteration:int) -> int:
        if(num_iteration <60):
             
            print("准备simulation，expansion后的棋盘状态是")
            print(node.state.render())
        #print("传入simulation时的颜色是：", node.action_colour)
        #new node，从action_list中随机选择一个action，然后apply到棋盘上，返回reward
        state = node.state
         
        if(num_iteration <= 50):
            #print("颜色是：", self._color)
            print(node.state.render())  
        #board_dict中取出.player是红色的棋子，然后re_num +1, 取出.player是蓝色的棋子，然后bl_num +1，决定下棋的是谁
        """
        red_count = 0
        blue_count = 0

        for cell in state._state.values():
            if cell.player == PlayerColor.RED:
                red_count += 1
            elif cell.player == PlayerColor.BLUE:
                blue_count += 1

        if red_count <= blue_count: #红色下棋
            colour = PlayerColor.RED
        else:
            colour = PlayerColor.BLUE #蓝色下棋 


        """
        if node.action_colour == PlayerColor.RED:
            colour = PlayerColor.BLUE
           # print("111111")
        else:
            colour = PlayerColor.RED
           # print("22222") 
        
        #if(num_iteration <=9):   
            #print("颜色变成：", colour)  
        action_list = self.get_action_list(state, colour)
        #if(num_iteration <= 9):   
          #  print("simulation 可以选择的action：", action_list)  
        #color = self._color
        #print("这是啥？？？？？？？？？？？: ", color) #蓝色 self.color 没变
        while not state.game_over:
           # print("颜色：", colour)  
            random_action = random.choice(action_list)
            
            #print("$$$$$$$模拟中选中的action: ", random_action)
            state.apply_action(random_action)
            #切换颜色
            if colour == PlayerColor.RED:
                colour = PlayerColor.BLUE
                #print("LINE 要找蓝色spread的: ", colour)
            else:
                colour = PlayerColor.RED 
                #print("LINE 要找红色可以spread的***********: ", colour)
            #print("颜色变成了：", colour) 
           # print(state.render())
            #获取新的action_list
            if node.state._total_power >= 48:
                #平局
                #print("平局,score = 0")
                #print("simulation 完成棋盘状态，在找哪个颜色的best_action: ",self._color)
                #print(state.render())
                return 0           
            action_list = self.get_action_list(state, colour)
        #游戏结束， 如果是红色胜利，返回1，否则返回-1
        #print("simulation 完成棋盘状态，在找哪个颜色的best_action: ",self._color)
        #print(state.render())
        if state.winner_color == PlayerColor.RED:
            #print("simulation 红色胜利,返回1")
            return 1
        else:
           # print("simulation 蓝色胜利，返回-1")
            return -1

         
         
    
    
    def backpropagation(self, node: Node, score: int, color:PlayerColor):
        #如果coulur == red, 说明当前要找红方的best action,score ==1,代表红方胜利，那么就是正分, 
        # score = -1,代表蓝色胜利，每次+= socre就是减分
        #更新当前节点的访问次数和得分
        if color == PlayerColor.RED:
            node.visits += 1
            node.wins += score
        else: #如果coulur == blue, 说明当前要找蓝方的best action,score == -1,代表蓝方胜利，那么就是-(-1)更新分数
            #score == 1,代表红方胜利，score 变成负的，减分
            score = score*(-1)
            node.visits += 1
            node.wins += score  
        #如果当前节点有父节点，则递归更新父节点
        if node.parent:
            self.backpropagation(node.parent, score, color)

      

    




        """
        #更新当前节点的访问次数和得分
        node.visits += 1
        node.wins += score
        #如果当前节点有父节点，则递归更新父节点
        if node.parent:
            backpropagation(node.parent, score) """

    def take_same_colour(self, board: Board, color:PlayerColor) -> list:
        same_colour_list = []
        for cell in board._state:
            if board._state[cell].player == color:
                same_colour_list.append(cell)
       # print("应该返回空的？因为当前场上没有蓝色的棋子")
        #print(same_colour_list)
        return same_colour_list

    def full_spread(self, list:list):
        #获取list中的每一个点，然后生成spread的6个方向的action
        #[HexPos(r=5, q=3), HexPos(r=6, q=4)]
        spread_action_list = []
        for cell in list:
            for direction in HexDir:
                spread_action_list.append(SpreadAction(cell, direction))
        return spread_action_list
    def take_empty_cell(self, board: Board) -> list:
        # given a board state, return a list of empty nodes
        #遍历整个字典，选择和coulor相同value的key
        empty_cell_list = []
        rmlist = []
        dir=[(0,1),(0,-1),(1,0),(-1,0),(1,-1),(-1,1)]
        #print(board._state)
        for cell in board._state:
            
            if(board._state[cell].player != self._color and board._state[cell].player != None):
                for direction in dir:
                    #print("direction: ",direction)
                    new_path = (cell.r, cell.q, direction[0], direction[1])
                    new_pos = self.spread_pos(new_path, board._state[cell].power)
                    #print("new_pos: ",new_pos)
                    rmlist.extend(new_pos)
                    #print("。。。。。。。。。。。。。。。。")
                    #print(rmlist)
                    #print(board._state)    
            if board._state[cell].player == None:
                empty_cell_list.append(cell)
        empty_cell_list=[k for k in empty_cell_list if k not in rmlist]
        #print("返回空棋盘,没有(3,3)")
        #print(empty_cell_list)
        return empty_cell_list
    
    def spread_pos(self,new_path,num): #point after spread
        new_pos = []
        x = new_path[0]
        y = new_path[1]
        for i in range(num):
            x = x +new_path[2]  # 4
            y = y+new_path[3] #7 ->0
        
            if(y > 6):
                y = 0
            if(y < 0):
                y = 6

            if(x > 6):
                x= 0
            if(x < 0):
                x = 6
            new_pos.append(HexPos(x,y))
        return new_pos    

        
    def fully_spawn(self, list:list):
        #given a list of empty nodes, return a list of SpawnAction objects
        spawn_action_list = []
        for cell in list:
            spawn_action_list.append(SpawnAction(cell))

        #print("返回一系列可以spawn的action,没有(3,3)")
        #print(spawn_action_list) [SpawnAction(cell=HexPos(r=6, q=0)), SpawnAction(cell=HexPos(r=5, q=0))]
        return spawn_action_list
 




    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the agent with the last player's action.
        """
        match action:
            case SpawnAction(cell):
                print(f"Testing: {color} SPAWN at {cell}")
                #def apply_action(self, action: Action):
                self.board.apply_action(action)
                print(self.board.render())
            case SpreadAction(cell, direction):
                print(f"Testing: {color} SPREAD from {cell}, {direction}")
                self.board.apply_action(action) #apply action to board 
                print(self.board.render())
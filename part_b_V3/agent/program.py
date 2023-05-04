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


  
    def mcts(self, board) -> Action:
        num_iterations = 2
       # print("***********************")
         
        root = Node(state=board) #初始化根节点,传入当前棋盘状态")
        while(num_iterations):         
           # print("num_iterations:",num_iterations)
            #print("新的iteration 开始了，root的棋盘状态，应该只有一个棋子")
           # print(board.render())
            lgeal_list =[]
            lgeal_list = self.get_action_list(root.state,self._color)
            # Selection
            select_node = self.selection(root,lgeal_list)
            #print("==================seletion 完成==================")

            # expansion, spread random_node的六个方向
            # *6 spread, + empty cell spawn, random返回一个下一步随机的一个新的点
            #print("--------slect_node.state--------------``````````````: \n", select_node.state.render())
            random_node = self.expansion(select_node)
            #print("==================expansion 完成==================")
            # Simulation
            socre = self.simulation(random_node)
            #print("==================esimulation 完成==================")
            #print(random_node.state._state)
            # Backpropagation
            self.backpropagation(random_node, socre, self._color)

           # print("==================回溯 完成==================")
  
            num_iterations -= 1 #递减

        #print("root目前生成了几个child:", len(root.children))  
        #for child in root.children:
            #print("child action:", child.action)
           # print("child_state:", child.state.render())

        best_child = root.best_child() #获取child里ucb1值最高的
        #print("返回的beast action是: ",best_child.action)
        return best_child.action

    
    


    def selection(self, node: Node, list: list) -> Optional[Node]:
        #print("检测sleection函数走了几次！！！！！！！")
        # 如果当前节点是终止节点或叶子节点，则返回当前节点
        if node.is_terminal() or node.is_leaf():
            #print("走这》》》》》》")
           # print("select node 输出棋盘状态")
           # print(node.state.render())
            return node
        #fully expanded
        if len(node.children) != len(list):
           # print("第二次走这》》》》》》")
            return node
        # 否则，选择最佳子节点进行扩展
        #print("无语住了》》》》》》")
        #print(node.best_child)
        return self.selection(node.best_child())

    def expansion(self, node: Node) -> Node:
        action_list = [] #store all possible actions including spawn and spread
        #print("查看传入expansion的棋盘状态应该是root的@@@@@@@@@@@@@@@@@@@@@@@@")
 
        match self._color:
            case PlayerColor.RED:
                action_list = self.get_action_list(node.state,self._color) #获取所有可能的action
                random_action = random.choice(action_list)#随机选择一个action
                new_state = copy.deepcopy(node.state) #deepcopy当前棋盘状态    
                if(node.state._total_power <= 48):
                    new_state.apply_action(random_action)#在新棋盘上执行这个action           
                
               # print("复制棋盘棋盘")
                #print(new_state.render())          
                new_node = Node(parent=node, state=new_state, action=random_action)#新建一个node，加入到children里
               # print("子节点的棋盘状态!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", new_node.state.render())
                #print("选择的随机动作动作: ", random_action)
                node.children.append(new_node)#将新建的node加入到children里
            
                #deepcopy new_node
                copy_node = copy.deepcopy(new_node)#deepcopy新建的node，供  simulation使用
                return copy_node  #返回新建的node
            case PlayerColor.BLUE:
                action_list = self.get_action_list(node.state,self._color)
                #print("action_list:", action_list)
                random_action = random.choice(action_list)
                new_state = copy.deepcopy(node.state)        
                if(node.state._total_power >= 48):
                    new_state.apply_action(random_action)#在新棋盘上执行这个action         
                new_state.apply_action(random_action)
                     
                new_node = Node(parent=node, state=new_state, action=random_action)
               #print("子节点的棋盘状态!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", new_node.state.render())
                #print("选择的随机动作动作: ", random_action)
                node.children.append(new_node)
            
                #deepcopy new_node
                copy_node = copy.deepcopy(new_node)
                return copy_node

    def get_action_list(self, board: Board, colour:PlayerColor) -> list:
        
        #print("执行action_list函数， 函数里的颜色是：", colour)
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
        spawn_action_list = self.fully_spawn(empty_cell_list)           
        action_list = spread_action_list + spawn_action_list 
        #print("action_list: ", action_list)
        #空一行
        #print()

        return action_list

    def simulation(self, node: Node) -> int:
        #print("准备simulation，目前的棋盘状态是")
        #print(node.state.render())
        #print("传入simulation时的颜色是：", self._color)
        #new node，从action_list中随机选择一个action，然后apply到棋盘上，返回reward
        state = node.state
        #print("颜色是：", colour)
        
        if self._color == PlayerColor.RED:
            colour = PlayerColor.BLUE
           # print("111111")
        else:
            colour = PlayerColor.RED
           # print("22222") 
           
        #print("颜色变成：", colour)  
        action_list = self.get_action_list(state, colour)
        #color = self._color
        #print("这是啥？？？？？？？？？？？: ", color) #蓝色 self.color 没变
        while not state.game_over:
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
            
           # print(state.render())
            #获取新的action_list
            if node.state._total_power >= 48:
                #平局
                print("平局,score = 0")
                #print("simulation 完成棋盘状态，在找哪个颜色的best_action: ",self._color)
                #print(state.render())
                return 0           
            action_list = self.get_action_list(state, colour)
        #游戏结束， 如果是红色胜利，返回1，否则返回-1
        #print("simulation 完成棋盘状态，在找哪个颜色的best_action: ",self._color)
        #print(state.render())
        if state.winner_color == PlayerColor.RED:
            print("simulation 红色胜利,返回1")
            return 1
        else:
            print("simulation 蓝色胜利，返回-1")
            return -1

         
         
    
    
    def backpropagation(slef, node: Node, score: int, color:PlayerColor):
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
            slef.backpropagation(node.parent, score, color)

      

    




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
                pass
            case SpreadAction(cell, direction):
                print(f"Testing: {color} SPREAD from {cell}, {direction}")
                self.board.apply_action(action) #apply action to board
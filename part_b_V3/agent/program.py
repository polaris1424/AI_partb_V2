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
                best_action = self.mcts(self.board)
                return best_action  


  
    def mcts(self, board) -> Action:
        num_iterations = 2
        print("***********************")
        print(board.render())
        root = Node(state=board) #初始化根节点,传入当前棋盘状态
        while(num_iterations):
            print("num_iterations:",num_iterations)
            # Selection
            select_node = self.selection(root)

            # expansion, spread random_node的六个方向
            # *6 spread, + empty cell spawn, random返回一个下一步随机的一个新的点
            random_node = self.expansion(select_node)

            # Simulation
            socre = self.simulation(random_node)
            # Backpropagation
            self.backpropagation(random_node, socre)
            
            
            
            num_iterations -= 1


        """
            # Backpropagation
            while node is not None:
                node.update(winner)
                node = node.parent """
    
    
    def selection(self, node: Node) -> Optional[Node]:
        # 如果当前节点是终止节点或叶子节点，则返回当前节点
        if node.is_terminal() or node.is_leaf():
            print("select node 输出棋盘状态")
            print(node.state.render())
            return node
        # 否则，选择最佳子节点进行扩展
        return self.selection(node.best_child())

    def expansion(self, node: Node) -> Node:
        action_list = [] #store all possible actions including spawn and spread
        print("!!!!!!!!!!!!!!!!!!expansion，下一行输出颜色")
        print(self._color)
        #查看棋盘状态
        print(node.state._state.keys())
        print(node.state._state[HexPos(r=3, q=3)])  #state 就是棋盘状态 CellState(RED, 1)
        print(node.state._state[HexPos(r=3, q=3)].player)    #颜色 RED
        #从当前棋盘获取颜色,如果是红子，获取棋盘上红子的位置,然后spread
        match self._color:
            case PlayerColor.RED:
                #action_list = self.get_action_list(node.state, self._color)
                same_colour_list = [] #存放同色的棋子
                same_colour_list = self.take_same_colour(node.state, self._color)
                #获取list中的每一个点，然后生成spread的6个方向的action
                spread_action_list = self.full_spread(same_colour_list)
                #获取棋盘上的空格，然后生成spawn的action
                empty_cell_list = self.take_empty_cell(node.state)
                #获取list中的每一个点，然后生成spread的6个方向的action
                spawn_action_list = self.fully_spawn(empty_cell_list)
                #合并两个list
                action_list = spread_action_list + spawn_action_list
                #随机返回一个action
                random_action = random.choice(action_list)
                #复制board
                new_state = copy.deepcopy(node.state)
                # 在copy_board 里apply action             
                new_state.apply_action(random_action)
                 # 将新节点添加到当前节点的子节点列表中
                new_node = Node(parent=node, state=new_state, action=random_action)
                print("新state 的 随机随机随机动作: ", random_action)
                # 在copy_board 里apply action 
                node.children.append(new_node)
                return new_node
            case PlayerColor.BLUE:
                #action_list = self.get_action_list(node.state, self._color)
                same_colour_list = [] #存放同色的棋子
                same_colour_list = self.take_same_colour(node.state, self._color)
                spread_action_list = self.full_spread(same_colour_list)
                empty_cell_list = self.take_empty_cell(node.state)     
                spawn_action_list = self.fully_spawn(empty_cell_list)           
                action_list = spread_action_list + spawn_action_list      
                random_action = random.choice(action_list)
                new_state = copy.deepcopy(node.state)                
                new_state.apply_action(random_action)
                print("复制棋盘棋盘")
                print(new_state.render())          
                new_node = Node(parent=node, state=new_state, action=random_action)
                print("新state 的 随机随机随机动作: ", random_action)
                node.children.append(new_node)
                return new_node

    def get_action_list(self, board: Board, color:PlayerColor) -> list:
        pass # expansion 获取List的那几步，spread和spawn

    def simulation(self, node: Node) -> int:
        #使用传入的node的棋盘，从action_list中随机选择一个action，然后apply到棋盘上，返回reward
        state = node.state
        action_list = self.get_action_list(state, self._color)
        color = self._color
        while not state.game_over:
            random_action = random.choice(action_list)
            state.apply_action(random_action)
            #切换颜色
            if color == PlayerColor.RED:
                color = PlayerColor.BLUE
            else:
                color = PlayerColor.RED
            #获取新的action_list
            action_list = self.get_action_list(state, color)
            #action_list = node.get_action_list(state, color)
        #游戏结束，获胜方
        return 1
    
    
    def backpropagation(node: Node, score: int):
        #更新当前节点的访问次数和得分
        node.visits += 1
        node.wins += score
        #如果当前节点有父节点，则递归更新父节点
        if node.parent:
            backpropagation(node.parent, score)

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
        for cell in board._state:
            if board._state[cell].player == None:
                empty_cell_list.append(cell)
        #print("返回空棋盘,没有(3,3)")
        #print(empty_cell_list)
        return empty_cell_list
        
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
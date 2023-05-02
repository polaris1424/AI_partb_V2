from math import log, sqrt
import random
from typing import Optional

from referee.game.actions import Action
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir
from referee.game.board import Board

class Node:
    def __init__(self, state: Board, parent=None, action=None):
        self.state = state  #当前节点的状态,当前棋盘状态
        self.parent =  parent #当前节点的父节点
        self.action = action #从父节点到当前节点的动作
        self.children = [] #当前节点的子节点
        self.wins = 0  #当前节点的胜利次数
        self.visits = 0  #当前节点的访问次数
        
        #self.HexPos = None #HexPos(3, 3) add postion of node
        #self.untried_actions = {} #当前节点的未扩展动作
        #self.player = None
    """    
    def selection(self, node: Node) -> Optional[Node]:
        # 如果当前节点是终止节点或叶子节点，则返回当前节点
        if node.is_terminal() or node.is_leaf():
            return node
        # 否则，选择最佳子节点进行扩展
        return self.selection(node.best_child())"""

    def is_leaf(self) -> bool:
        return len(self.children) == 0

    
    def is_terminal(self) -> bool:
        return self.state.game_over #判断当前节点是否是终止节点

 
    def best_child(self):
        #返回当前节点的最佳子节点
        #UCB1算法
        best_child = None #最佳子节点
        best_score = -1 #最佳子节点的UCB1值
        for child in self.children:
            score = child.wins / child.visits + 2 * sqrt(log(self.visits) / child.visits)#UCB1算法
            if score > best_score: #更新最佳子节点
                best_score = score #更新最佳子节点的UCB1值
                best_child = child #更新最佳子节点
        return best_child
 
    def best_child(self):
        # 返回当前节点的最佳子节点
        # UCB1算法
        best_child = None  # 最佳子节点
        best_score = -1  # 最佳子节点的UCB1值
        for child in self.children:
            if child.visits == 0: # 如果当前子节点没有被访问过，直接返回该子节点
                return child
            score = child.wins / child.visits + 2 * sqrt(log(self.visits) / child.visits)  # UCB1算法
            if score > best_score:  # 更新最佳子节点
                best_score = score  # 更新最佳子节点的UCB1值
                best_child = child  # 更新最佳子节点
            elif score == best_score:  # 如果UCB1值相等，随机选择一个子节点
                best_child = random.choice([best_child, child])
        return best_child

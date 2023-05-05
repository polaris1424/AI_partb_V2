
"""
        
    def action(self, **referee: dict) -> Action:
        match self._color:
            case PlayerColor.RED:           
                if self.board._state == {}: #empty board
                    print("!!!!!!!!!!!!空")
                    return SpawnAction(HexPos(3, 3))
                else:
                    best_action = self.mcts(self.board)
                    return best_action

            case PlayerColor.BLUE:
               
                if self.board._state == {}: #empty board
                     return SpawnAction(HexPos(3, 3))
                else:
                 
                    best_action = self.mcts(self.board)
                    return best_action
  
    def mcts(self, board) -> Action:
        num_iterations = 2
        root = Node(state=board) #初始化根节点,传入当前棋盘状态")
        while(num_iterations):         
            lgeal_list =[]
            lgeal_list = self.get_action_list(root.state,self._color)
            # Selection
            select_node = self.selection(root,lgeal_list)
            random_node = self.expansion(select_node)
            socre = self.simulation(random_node)
            self.backpropagation(random_node, socre, self._color) 
            num_iterations -= 1 #递减
        best_child = root.best_child() #获取child里ucb1值最高的
        return best_child.action
 
    def selection(self, node: Node, list: list) -> Optional[Node]:
        if node.is_terminal():
            return node        
        if node.is_leaf():
           return node
        if len(node.children) != len(list):     
            return node
        return self.selection(node.best_child())

    def expansion(self, node: Node) -> Node:
        action_list = [] #store all possible actions including spawn and spread
        match self._color:
            case PlayerColor.RED:
                action_list = self.get_action_list(node.state,self._color) #获取所有可能的action
                random_action = random.choice(action_list)#随机选择一个action
                new_state = copy.deepcopy(node.state) #deepcopy当前棋盘状态    
                if(node.state._total_power <= 48):
                    new_state.apply_action(random_action)#在新棋盘上执行这个action            
                new_node = Node(parent=node, state=new_state, action=random_action)#新建一个node，加入到children里
                node.children.append(new_node)#将新建的node加入到children里
                #deepcopy new_node
                copy_node = copy.deepcopy(new_node)#deepcopy新建的node，供  simulation使用
                return copy_node  #返回新建的node
            case PlayerColor.BLUE:
                action_list = self.get_action_list(node.state,self._color)
                random_action = random.choice(action_list)
                new_state = copy.deepcopy(node.state)        
                if(node.state._total_power <= 48):
                    new_state.apply_action(random_action)#在新棋盘上执行这个action        
                     
                new_node = Node(parent=node, state=new_state, action=random_action)
                node.children.append(new_node)
                copy_node = copy.deepcopy(new_node)
                return copy_node

    def get_action_list(self, board: Board, colour:PlayerColor) -> list:
        same_colour_list = [] #存放同色的棋子
        same_colour_list = self.take_same_colour(board, colour)
        spread_action_list = self.full_spread(same_colour_list)
        empty_cell_list = self.take_empty_cell(board)     
        spawn_action_list = self.fully_spawn(empty_cell_list)           
        action_list = spread_action_list + spawn_action_list 
        return action_list

    def simulation(self, node: Node) -> int:
        state = node.state
        if self._color == PlayerColor.RED:
            colour = PlayerColor.BLUE
        else:
            colour = PlayerColor.RED
        action_list = self.get_action_list(state, colour)
        while not state.game_over:
           
            random_action = random.choice(action_list)
            state.apply_action(random_action)
            #切换颜色
            if colour == PlayerColor.RED:
                colour = PlayerColor.BLUE    
            else:
                colour = PlayerColor.RED     
            #获取新的action_list
            if node.state._total_power >= 48:
                return 0           
            action_list = self.get_action_list(state, colour)
      
        if state.winner_color == PlayerColor.RED:
            print("simulation 红色胜利,返回1")
            return 1
        else:
            print("simulation 蓝色胜利，返回-1")
            return -1
    def backpropagation(slef, node: Node, score: int, color:PlayerColor):  
        if color == PlayerColor.RED:
            node.visits += 1
            node.wins += score
        else: #如果coulur == blue, 说明当前要找蓝方的best action,score == -1,代表蓝方胜利，那么就是-(-1)更新分数
            score = score*(-1)
            node.visits += 1
            node.wins += score  
         
        if node.parent:
            slef.backpropagation(node.parent, score, color)
 
    def take_same_colour(self, board: Board, color:PlayerColor) -> list:
        same_colour_list = []
        for cell in board._state:
            if board._state[cell].player == color:
                same_colour_list.append(cell)
       
        return same_colour_list

    def full_spread(self, list:list):
         
        spread_action_list = []
        for cell in list:
            for direction in HexDir:
                spread_action_list.append(SpreadAction(cell, direction))
        return spread_action_list
    def take_empty_cell(self, board: Board) -> list:      
        empty_cell_list = []
        rmlist = []
        dir=[(0,1),(0,-1),(1,0),(-1,0),(1,-1),(-1,1)]
       
        for cell in board._state:
            
            if(board._state[cell].player != self._color and board._state[cell].player != None):
                for direction in dir:
                     
                    new_path = (cell.r, cell.q, direction[0], direction[1])
                    new_pos = self.spread_pos(new_path, board._state[cell].power)
                   
                    rmlist.extend(new_pos)
                  
            if board._state[cell].player == None:
                empty_cell_list.append(cell)
        empty_cell_list=[k for k in empty_cell_list if k not in rmlist]
         
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
       
        spawn_action_list = []
        for cell in list:
            spawn_action_list.append(SpawnAction(cell))      
        return spawn_action_list
 """
 
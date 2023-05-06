"""
    def mcts(self, board) -> Action:
        num_iterations = 50
        root = Node(state=board) #初始化根节点,传入当前棋盘状态")      
        while(num_iterations):                           
            legal_list =[]        
            select_node, legal_list = self.selection(root) #action_num是当前root的action数量,用于判断是否fully expande        
            random_node = self.expansion(select_node,legal_list)  #update legal_list,remove random_node      
            socre = self.simulation(random_node)     
            self.backpropagation(random_node, socre, self._color)
            num_iterations -= 1 #递减     
        best_child = root.best_child() #获取child里ucb1值最高的    
        return best_child.action

  
    def selection(self, node: Node) -> Optional[Node]: 
        legal_list = self.get_action_list(node.state,self._color)
        num = len(legal_list)
        if node.is_terminal():          
            for child in node.children:
                if child.action in legal_list:
                    legal_list.remove(child.action)
            return node,legal_list  
        if node.is_leaf():          
            for child in node.children:
                if child.action in legal_list:
                    legal_list.remove(child.action)
            return node,legal_list          
        #fully expanded
        if len(node.children) != num:  #如果当前节点的所有子节点还没被扩展过了
           
            for child in node.children:
                if child.action in legal_list:
                    legal_list.remove(child.action)
            return node,legal_list
        return self.selection(node.best_child())


    def expansion(self, node: Node, legal_list:list[Action]) -> Node:
        match self._color:
            case PlayerColor.RED:
              
                random_action = random.choice(legal_list)#随机选择一个action
                new_state = copy.deepcopy(node.state) #deepcopy当前棋盘状态    
                if(node.state._total_power <= 48):
                    new_state.apply_action(random_action)#在新棋盘上执行这个action                 
                new_node = Node(parent=node, state=new_state, action=random_action)#新建一个node，加入到children里           
                node.children.append(new_node)#将新建的node加入到children里      
                #deepcopy new_node
                copy_node = copy.deepcopy(new_node)#deepcopy新建的node，供  simulation使用
                return copy_node#返回新建的node
            case PlayerColor.BLUE:           
                random_action = random.choice(legal_list)
                new_state = copy.deepcopy(node.state)        
                if(node.state._total_power <= 48):
                    new_state.apply_action(random_action)#在新棋盘上执行这个action                     
                new_node = Node(parent=node, state=new_state, action=random_action) #新建一个node，加入到children里 
                node.children.append(new_node)    
                #deepcopy new_node
                copy_node = copy.deepcopy(new_node) #deepcopy新建的node，供  simulation使用  
                return copy_node   #返回新建的node
"""
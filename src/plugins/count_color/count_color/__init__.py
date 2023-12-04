"""
This is where the implementation of the plugin code goes.
The count_color-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import logging
from webgme_bindings import PluginBase

# Setup a logger
logger = logging.getLogger('count_color')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)  # By default it logs to stderr..
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class count_color(PluginBase):
  def main(self):
    active_node = self.active_node
    self.namespace=''
    core = self.core
    logger = self.logger
    logger.debug('path: {0}'.format(core.get_path(active_node)))
    logger.info('name: {0}'.format(core.get_attribute(active_node, 'name')))
    logger.warn('pos : {0}'.format(core.get_registry(active_node, 'position')))
    logger.error('guid: {0}'.format(core.get_guid(active_node)))
    nodesList = core.load_sub_tree(active_node)                                          
    nodes = {}  
    for node in nodesList:      
       nodes[core.get_path(node)] = node  
    self.nodes=nodes
    logger.info(self.count_color('black'))
    #logger.info(self.active_tiles())
    #logger.info('Ths is our last piece played : {0}'.format(core.get_attribute(nodes[core.get_pointer_path(active_node,'lastPiece')],'Piece')))
    #self.flip_lastpiece()
    #next_gs=core.get_pointer_path
    #logger.info('This is the next Gamestate : {0}'.format(next_gs))
    
    
  def active_tiles(self):
    
    def check_valid(tile):
         import math        
         active_node = tile   
         core = self.core             
         logger = self.logger    
         self.namespace = None    
         META = self.META      
         
         board=core.get_parent(active_node)
         gamestate=core.get_parent(board)
         nodesList = core.load_sub_tree(gamestate) 

         nodes = {}  

         for node in nodesList:      
             nodes[core.get_path(node)] = node  


         state = {}        
         state['name'] = core.get_attribute(gamestate, 'name')        
         logger.info(state)        
         cp_path=core.get_pointer_path(gamestate, 'currentPlayer')        
         if cp_path!=None :           
            state['currentPlayer'] = core.get_attribute(nodes[cp_path],'name')        
         else :           
            state['currentPlayer']=None 
         
         row=core.get_attribute(active_node,'row')
         column=core.get_attribute(active_node,'column')
         #logger.info("{0},{1} is the tile".format(row,column))
         state['currentMove']={'row':row,'column':column}        
                
         #row = [{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'}]        
         board = [[{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'}]
                  , [{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'}]
                  , [{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'}]
                  ,[{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'}]
                  , [{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'}]
                  , [{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'}]
                  , [{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'}]
                  , [{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'}]
                 ]        
         for child in core.get_children_paths(gamestate):          
            if (core.is_instance_of(nodes[child], META['Board'])):            
                for tile in core.get_children_paths(nodes[child]):              
                    for piece in core.get_children_paths(nodes[tile]):
                        #logger.info("{0} at {1},{2}".format(core.get_attribute(nodes[piece],'color'),core.get_attribute(nodes[tile],'row'),core.get_attribute(nodes[tile],'column')))
                        
                        board[core.get_attribute(nodes[tile],'row')][core.get_attribute(nodes[tile],'column')]['color'] = core.get_attribute(nodes[piece],'color')
                        #logger.info(board)
         state['board'] = board
         #logger.info(state)

         

         def tile_exist(tile,rmax,cmax):       
            return rmax<tile[0] or tile[1]>cmax or tile[0]<0 or tile[1]<0 
                
         def check_logic(state):
            player=state['currentPlayer']
            currentMove=state['currentMove']
            board=state['board']
            currentColor='black'
            if player=='PlayerBlack':
              currentColor='white'
          
            if currentMove == None :         
                return False            
            row=currentMove['row']    
            col=currentMove['column']      
                
            oppColor='Dont know'      
            if currentColor == 'black':        
                oppColor='white'      
            elif currentColor == 'white':        
                oppColor='black'      
            k=0      
            dirs=[(row,col+k),(row+k,col),(row,col-k),(row-k,col),(row+k,col+k),(row+k,col-k),(row-k,col+k),(row-k,col-k)]      
            state=[-1,-1,-1,-1,-1,-1,-1,-1]      
            valid=[False,False,False,False,False,False,False,False]      
            result=False 
            #logger.info('Currentcolor : {0}'.format(currentColor))
            #logger.info("Tiles Now : {0}".format(dirs))  
            #logger.info(any([not math.isinf(x) for x in state]))
            while any([not math.isinf(x) for x in state]) :        
                k=k+1        
                dirs=[(row,col+k),(row+k,col),(row,col-k),(row-k,col),(row+k,col+k),(row+k,col-k),(row-k,col+k),(row-k,col-k)]        
                #logger.info("Tile's considered : {0}".format(dirs))        
                ("States : {0}".format(state))        
                # #logger.info("Are all infinities : {0}".format([not math.isinf(x) for x in state]))        
                #logger.info("Sum of infinites : {0}".format(any([not math.isinf(x) for x in state])))        
                color_vec=[]
                
                #transition functions for all 8 directions
                for i in range(len(state)):                    
                    #logger.info("exploring new horizon.")          
                    # #logger.info("\t\t\t Piece being Considerd row : {0},column : {1}".format(dirs[i][0],dirs[i][1]))          
                    # #logger.info("\t\t\t Piece Color {0}".format(board[dirs[i][0]][dirs[i][1]]['color']))          
                    # #logger.info("\t\t\t Direction state {0}".format(state[i]))          
                    # #logger.info("\t\t\t Opposite color : {0}".format(oppColor))         
                    #  #logger.info("\t\t\t Current color : {0}".format(currentColor))          
                        # #logger.info("\t\t\t State's Now : {0}".format(state)) 
                    
                    if tile_exist(dirs[i],7,7) : #goes to -infinity when out of board          
                        state[i]=float('-inf')          
                    elif board[dirs[i][0]][dirs[i][1]]['color']=="none": #goes to -infinity when empty tile          
                        state[i]=float('-inf')          
                    elif  math.isinf(state[i]): #goes to -infinity when prev tile is empty          
                        state[i]=float('-inf')          
                    elif board[dirs[i][0]][dirs[i][1]]['color']==oppColor: #when we find opps colr           
                        state[i]=0          
                    elif board[dirs[i][0]][dirs[i][1]]['color']==currentColor and state[i]==0: #opps_color->current_color           
                        state[i]=1                
                    
                #logger.info("State's considered : {0}".format(state))     
                                    
                for i in range(len(valid)):          
                    if state[i]>0:            
                        valid[i]=True          
                    else :            
                        valid[i]=False          
                    result=result or valid[i]        
                    if result==True:          
                        return result      
                print(f"Valid : {valid}")
                print(f"Result is {result}")
            return result     
                
         return check_logic(state)
    
    valid_tiles=[]
    cp_list=self.core.get_children_paths(self.active_node)
    self.logger.info('Childs of Game State {0}'.format(cp_list))
    for cp in cp_list:
      child=self.nodes[cp]
      if (self.core.is_instance_of(child, self.META['Board'])):
        for tile in self.core.get_children_paths(self.nodes[cp]):
          tile=self.nodes[tile]
          f=self.core.get_attribute(tile,'pythonCode')
          row=self.core.get_attribute(tile,'row')
          column=self.core.get_attribute(tile,'column')
          #self.logger.info("{0},{1} is the tile".format(row,column))
          #self.logger.info('Tile python code : {0}'.format(f))
          if row is None or column is None :
            continue
          elif check_valid(tile):
            valid_tiles.append(child)
    return valid_tiles        
   
    
  def count_color(self,color):
    color_count=0
    cp_list=self.core.get_children_paths(self.active_node)
    
    #self.logger.info('Childs of Game State {0}'.format(self.core.get_attribute(cp_list,'name')))
    for cp in cp_list:
      child=self.nodes[cp]
      #self.logger.info('Childs of Game State {0}'.format(self.core.get_attribute(child,'name')))
      #self.META['Board']
      if (self.core.is_instance_of(child, self.META['Board'])):
        for tile in self.core.get_children_paths(child):
          #self.logger.info(tile)
          tile=self.nodes[tile]
          for piece_path in self.core.get_children_paths(tile):
            piece=self.nodes[piece_path]
            if color==self.core.get_attribute(piece,'color'):
              color_count=color_count+1
    return color_count
  
  def flip_lastpiece(self):
    last_piece=self.nodes[self.core.get_pointer_path(self.active_node,'lastPiece')]
    last_tile=self.core.get_parent(last_piece)
    
    
    def check_valid(tile):
         
         import math        
         active_node = tile   
         core = self.core             
         logger = self.logger    
         self.namespace = None    
         META = self.META      
         logger.info('Current Node : {0},{1}'.format(core.get_attribute(active_node,'row'),core.get_attribute(active_node,'column')))
         board=core.get_parent(active_node)
         gamestate=core.get_parent(board)
         nodesList = core.load_sub_tree(gamestate)                                          
         nodes = {}  

         for node in nodesList:      
             nodes[core.get_path(node)] = node  


         state = {}        
         state['name'] = core.get_attribute(gamestate, 'name')        
         logger.info(state)        
         cp_path=core.get_pointer_path(gamestate, 'currentPlayer')        
         if cp_path!=None :           
            state['currentPlayer'] = core.get_attribute(nodes[cp_path],'name')        
         else :           
            state['currentPlayer']=None 
         row=core.get_attribute(active_node,'row')
         column=core.get_attribute(active_node,'column')
         state['currentMove']={'row':row,'column':column}        
                
         #row = [{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'}]        
         board = [[{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'}]
                  , [{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'}]
                  , [{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'}]
                  ,[{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'}]
                  , [{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'}]
                  , [{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'}]
                  , [{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'}]
                  , [{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'},{'color':'none'}]
                 ]        
         for child in core.get_children_paths(gamestate):          
            if (core.is_instance_of(nodes[child], META['Board'])):            
                for tile in core.get_children_paths(nodes[child]):              
                    for piece in core.get_children_paths(nodes[tile]):
                        #logger.info("{0} at {1},{2}".format(core.get_attribute(nodes[piece],'color'),core.get_attribute(nodes[tile],'row'),core.get_attribute(nodes[tile],'column')))
                        
                        board[core.get_attribute(nodes[tile],'row')][core.get_attribute(nodes[tile],'column')]['color'] = core.get_attribute(nodes[piece],'color')
                        #logger.info(board)
         state['board'] = board
         #logger.info(state)
         #logger.info(core.get_parent(gamestate))
       
          
          
          
         next_gs = core.copy_node(gamestate,core.get_parent(gamestate))
         core.set_pointer(self.active_node,'next',next_gs)
         next_name=core.get_attribute(gamestate,'name')+str(1)
         core.set_attribute(gamestate,'name',next_name)
         next_nodes={}
         for node in core.load_sub_tree(next_gs) :      
             next_nodes[core.get_path(node)] = node 
        
         def set_nextPlayer(next_gs,next_nodes):
            cp_path=core.get_pointer_path(next_gs,'currentPlayer')
            cp=next_nodes[cp_path]
            for c in core.get_children_paths(next_gs):
              child=next_nodes[c]
              if(core.is_instance_of(child,META['Player']) and child!=cp):
                core.set_pointer(next_gs,'currentPlayer',child)
                np_path=core.get_pointer_path(next_gs,'currentPlayer')
                np=next_nodes[np_path]                
                return core.get_attribute(np,'color')
         
         def set_nextMove(next_gs,next_nodes,pos,player_color):
            next_board=None
            for c in core.get_children_paths(next_gs):
              child=next_nodes[c]
              if(core.is_instance_of(child,META['Board'])):
                next_board=child
              
            for tile in core.get_children_paths(next_board):
              tile=next_nodes[tile]
              next_pos=(core.get_attribute(tile,'row'),core.get_attribute(tile,'column'))
              if next_pos==pos : 
                next_piece=core.create_child(tile,META['Piece'])#usingcopy_node to create a new node
                next_nodes[core.get_path(next_piece)]=next_piece#added piece to next_nodes
                core.set_attribute(next_piece,'color',player_color)
                core.set_pointer(next_gs,'currentMove',next_piece)
                nm_path=core.get_pointer_path(next_gs,'currentMove')
                nm=next_nodes[nm_path]
                return core.get_attribute(nm,'color')
              
         def flip_tiles(next_gs,next_nodes,ft,player_color):
            next_board=None
            flipped_tiles=[]
            for c in core.get_children_paths(next_gs):
              child=next_nodes[c]
              if(core.is_instance_of(child,META['Board'])):
                next_board=child
              
            for tile in core.get_children_paths(next_board):
              tile=next_nodes[tile]
              next_pos=(core.get_attribute(tile,'row'),core.get_attribute(tile,'column'))
              for t in ft :
                if t==next_pos:
                  flip_piece=next_nodes[core.get_children_paths(tile)[0]]
                  core.set_attribute(flip_piece,'color',player_color)
                  flipped_tiles.append(tile)
            return flipped_tiles 
                
            #set_currentMove pointer
         pos=(row,column)
         player_color= core.get_attribute(nodes[cp_path],'color')
         if player_color =='black':
          player_color='white'
         else :
          player_color='black'
         
        
          
        
         def tile_exist(tile,rmax,cmax):       
            return rmax<tile[0] or tile[1]>cmax or tile[0]<0 or tile[1]<0 
                
         def check_logic(state):
            tile_flip=[]
            player=state['currentPlayer']
            currentMove=state['currentMove']
            board=state['board']
            currentColor='black'
            if player=='PlayerBlack':
              currentColor='white'
          
            if currentMove == None :         
                return False            
            row=currentMove['row']    
            col=currentMove['column']      
                
            oppColor='Dont know'      
            if currentColor == 'black':        
                oppColor='white'      
            elif currentColor == 'white':        
                oppColor='black'      
            k=0 
            dir_keys=[]
            dirs=[(row,col+k),(row+k,col),(row,col-k),(row-k,col),(row+k,col+k),(row+k,col-k),(row-k,col+k),(row-k,col-k)]      
            state=[-1,-1,-1,-1,-1,-1,-1,-1]      
            valid=[False,False,False,False,False,False,False,False] 
            tile_flip_dir=[[] for x in range(len(state))]
            result=False 
            #logger.info('Currentcolor : {0}'.format(currentColor))
            #logger.info("Tiles Now : {0}".format(dirs))  
            #logger.info(any([not math.isinf(x) for x in state]))
            while any([not math.isinf(x) for x in state]) :        
                k=k+1        
                dirs=[(row,col+k),(row+k,col),(row,col-k),(row-k,col),(row+k,col+k),(row+k,col-k),(row-k,col+k),(row-k,col-k)]        
                #logger.info("Tile's considered : {0}".format(dirs))        
                ("States : {0}".format(state))        
                # #logger.info("Are all infinities : {0}".format([not math.isinf(x) for x in state]))        
                #logger.info("Sum of infinites : {0}".format(any([not math.isinf(x) for x in state])))        
                color_vec=[]
                
                #transition functions for all 8 directions
                for i in range(len(state)):                    
                    #logger.info("exploring new horizon.")          
                    # #logger.info("\t\t\t Piece being Considerd row : {0},column : {1}".format(dirs[i][0],dirs[i][1]))          
                    # #logger.info("\t\t\t Piece Color {0}".format(board[dirs[i][0]][dirs[i][1]]['color']))          
                    # #logger.info("\t\t\t Direction state {0}".format(state[i]))          
                    # #logger.info("\t\t\t Opposite color : {0}".format(oppColor))         
                    #  #logger.info("\t\t\t Current color : {0}".format(currentColor))          
                        # #logger.info("\t\t\t State's Now : {0}".format(state)) 
                    
                    if tile_exist(dirs[i],7,7) : #goes to -infinity when out of board          
                        state[i]=float('-inf')          
                    elif board[dirs[i][0]][dirs[i][1]]['color']=="none": #goes to -infinity when empty tile          
                        state[i]=float('-inf')          
                    elif  math.isinf(state[i]): #goes to -infinity when prev tile is empty          
                        state[i]=float('-inf')          
                    elif board[dirs[i][0]][dirs[i][1]]['color']==oppColor: #when we find opps colr           
                        state[i]=0 
                        tile_flip_dir[i].append((dirs[i][0],dirs[i][1]))
                    elif board[dirs[i][0]][dirs[i][1]]['color']==currentColor and state[i]==0: #opps_color->current_color           
                        state[i]=1
                        tile_flip.extend(tile_flip_dir[i])
                    
                #logger.info("State's considered : {0}".format(state))     
                                    
                for i in range(len(valid)):          
                    if state[i]>0:            
                        valid[i]=True          
                    else :            
                        valid[i]=False          
                    result=result or valid[i]        
                    if result==True:          
                        return result,tile_flip      
                print(f"Valid : {valid}")
                print(f"Result is {result}")
            return result,tile_flip 
          
         logger.info('{0} is the next player'.format(set_nextPlayer(next_gs,next_nodes)))
         logger.info('{0} is the next move'.format(set_nextMove(next_gs,next_nodes,pos,player_color)))       
         result,ft_pos=check_logic(state)
         ft=flip_tiles(next_gs,next_nodes,ft_pos,player_color)
         logger.info(ft)
         for t in ft:
          flip_piece=next_nodes[core.get_children_paths(t)[0]]
          piece_color=core.get_attribute(flip_piece,'color')
          logger.info('{0},{1} is the tile with color {2}'.format(core.get_attribute(t,'row'),core.get_attribute(t,'column'),piece_color))   
         
         if result : 
          self.util.save(self.root_node,self.commit_hash,self.branch_name)
          logger.info('Is a valid move')
         else : 
          logger.error('Not a Valid Move')
         return   check_logic(state)
    check_valid(last_tile)
    
    def undo(self):
      game_folder=self.core.get_parent(self.active_node)
      
      nodesList = core.load_sub_tree(game_folder)                                          
      nodes = {}  

      for node in nodesList:      
           nodes[core.get_path(node)] = node 
      
      prev_state_path=self.core.get_pointer_path(self.active_node,'prev')
      prev_state=self.nodes[prev_state]#doubtfull
      self.core_set_pointer(game_folder,'currentState',prev_state)
      self.core.delete_node(self.active_node)
      self.util.save(self.root_node,self.commit_hash,self.branch_name)
      
    


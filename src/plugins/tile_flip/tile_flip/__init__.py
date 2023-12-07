"""
This is where the implementation of the plugin code goes.
The tile_flip-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import logging
from webgme_bindings import PluginBase

# Setup a logger
logger = logging.getLogger('tile_flip')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)  # By default it logs to stderr..
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class tile_flip(PluginBase):
  def main(self):
    active_node = self.active_node
    core = self.core
    logger = self.logger
    logger.debug('path: {0}'.format(core.get_path(active_node)))
    logger.info('name: {0}'.format(core.get_attribute(active_node, 'name')))
    logger.warn('pos : {0}'.format(core.get_registry(active_node, 'position')))
    logger.error('guid: {0}'.format(core.get_guid(active_node)))
    tile=self.active_node
    logger.info(self.check_valid())

   
  def check_valid(self):
         
         import math        
         active_node = self.active_node   
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
         logger.info(state['board'])
         #logger.info(core.get_parent(gamestate))
       
         logger.info("Gamestate nodepath before next{0}".format(gamestate["nodePath"]))
          
          
         next_gs = core.copy_node(gamestate,core.get_parent(gamestate))
         core.set_pointer(self.active_node,'next',next_gs)
         next_name=core.get_attribute(gamestate,'name')+str(1)
         core.set_attribute(next_gs,'name',next_name)
         next_nodes={}
         logger.info("Gamestate nodepath after next{0}".format(gamestate["nodePath"]))
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
              logger.debug(tile['nodePath'])
              logger.debug(next_gs['nodePath'])
              next_pos=(core.get_attribute(tile,'row'),core.get_attribute(tile,'column'))
              if next_pos==pos : 
                next_piece=core.create_child(tile,META['Piece'])#usingcopy_node to create a new node
                #self.logger.info("Tile where piece will be created : {0},{1}".format(pos[0],pos[1]))
                
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

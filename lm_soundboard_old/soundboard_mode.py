'''
Created on Jun 14, 2016

@author: joel
'''
from lm_soundboard_old.launchpad_mode import mode
# import zmq
from lm_soundboard_old.constants import OFF, AMBER, GREEN_FLASHING, GREEN, RED
from threading import Thread
import swmixer
from lm_soundboard_old.button import Gridbutton
#import wav_thread

class Soundboardmode(mode):
    '''
    classdocs
    '''


    def __init__(self, controller):
        '''
        Constructor
        '''
        
       
        
        
#         #get zmq context from controller
#         self.ctx = controller.ctx
        
                       
        self.controller = controller
        self.conf = self.controller.conf
        self.sound_path = self.conf["sound_path"]
        self.grid = {}
        
        
    def on_enter_mode(self):
        conf = self.controller.conf
        #(Re-)load the grid from the current in-memory config
        self.grid = {}        
        for ID,options in conf['grid'].items():
            self.grid[ID] = Gridbutton(ID, self, **options)
            self.controller.change_grid_color(ID,AMBER)
#                 self.add_button(int(ID), *options)
        
    def on_exit_mode(self):
        
        for ID, button in self.grid.items():
#             self.controller.send_message([ID,'DESTROY'])
            button.stop()
            self.controller.change_grid_color(ID,OFF)
            
        
            
        
    def on_grid_button_pressed(self, ID):
        grid = self.grid
        
        if ID in grid:
            
            color = grid[ID].on_press()
            if color is not None:
                self.controller.change_grid_color(ID,color)
            
#             if grid[ID]['state'] == 'PLAYING':
#                 if grid[ID]['mode'] == 'LOOP':
#                     #Do not repeat track when it finishes
#                     grid[ID]['state'] = 'STOPPING'
#                     #Give visual feedback that the track is stopping
#                     self.controller.change_grid_color(ID, GREEN_FLASHING)
#                 else:
#                     #tell thread with corresponding id to pause
#                     self.controller.send_message([ID,'PAUSE'])
#                     #update status
#                     grid[ID]['state'] = 'PAUSED'                            
#                     #set the corresponding LED to amber
#                     self.controller.change_grid_color(ID , AMBER)
#             else:
#                 #tell thread with corresponding id to play
#                 self.controller.send_message([ID,'PLAY'])
#                
#                 #update status
#                 grid[ID]['state'] = 'PLAYING'
#                 #set the corresponding LED to green
#                 self.controller.change_grid_color(ID , GREEN)
        else:
            #Give visual feedback, that the button is unassigned
            self.controller.change_grid_color(ID,RED)
            
    def on_grid_button_released(self, ID):
        if ID in self.grid:
            #For assigned buttons, actions happen on button down, so do nothing here
            pass
        else:
            #The button pressed was unassigned, remove visual feedback on release
            self.controller.change_grid_color(ID,OFF)
            
    def add_button(self,ID,soundfile,mode='DEFAULT'):
        
#         t1 = Thread(target=wav_thread.main,args=(self.sound_path + soundfile, self.ctx, ID))
#         t1.setDaemon(True)
        #track play state and mode of the button
        self.grid[ID] = {}
        self.grid[ID]['sound'] = swmixer.Sound(soundfile)        
        self.grid[ID]['state'] = 'STOPPED'
        self.grid[ID]['mode'] = mode
#         t1.start()
        #Light up the corresponding LED in AMBER
        self.controller.change_grid_color(ID , AMBER)
        
        
    def on_stop(self, ID):
        self.controller.change_grid_color(ID,AMBER)
        
    def on_pause(self, ID):
        self.controller.change_grid_color(ID,AMBER)
            
                
#     def on_message(self, multipart):
#         grid = self.grid
#         ID,message = multipart
#         ID = ID
#         if message == 'FINISHED':
#             #Sound file finished playing
#             if (grid[ID]['mode'] == 'LOOP' or grid[ID]['mode'] == 'LOOP_PAUSABLE' ) \
#             and grid[ID]['state'] != 'STOPPING':
#                 #restart the file immediately
#                 self.controller.send_message([ID,'RESTART'])
#             else:
#                 #update status                    
#                 grid[ID]['state'] = 'STOPPED'
#                 #set LED back to Amber
#                 self.controller.change_grid_color(ID,AMBER)
                

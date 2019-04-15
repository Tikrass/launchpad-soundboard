'''
Created on Jun 16, 2016

@author: joel
'''
from lm_soundboard_old.launchpad_mode import mode

from lm_soundboard_old.constants import *


class Deletemode(mode):
    '''
    classdocs
    '''


    def __init__(self, controller):
        '''
        Constructor
        '''
        self.controller = controller
        self.selected = None
        
        
    def on_enter_mode(self):
        self.conf = self.controller.conf
        self.grid = self.conf['grid']
        self.selected = None
        #Light up all assigned buttons
        for ID in self.grid:
                self.controller.change_grid_color(ID,AMBER)
                
    def on_exit_mode(self):
        self.selected = None
                
    def on_grid_button_pressed(self, ID):
        if self.selected is None and ID in self.grid:
            #Select this button for deletion, light up the button and wait for confirmation
            self.selected = ID
            self.controller.change_grid_color(ID,RED_FLASHING)
        else:
            if self.selected == ID:
                #Deletion confirmed
                del(self.grid[ID])
                self.controller.change_grid_color(self.selected,OFF)
                self.selected = None
            elif self.selected is not None:
                #Abort
                self.controller.change_grid_color(self.selected,AMBER)
                self.selected = None

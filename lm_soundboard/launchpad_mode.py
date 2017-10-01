'''
Created on Jun 14, 2016

@author: joel
'''



class mode(object):
    '''
    classdocs
    '''


    def __init__(self, controller):
        '''
        Constructor
        '''
    
    def on_enter_mode(self):
        pass
    
    def on_exit_mode(self):
        pass
        
    def on_grid_button_pressed(self,ID):
        pass 
    def on_grid_button_released(self,ID):
        pass 
    
    #Live Buttons are on the top row of buttons
    def on_live_button_pressed(self,ID):
        pass
    def on_live_button_released(self,ID):
        pass
    
    #Special Buttons are on the right hand side of the launchpad
    def on_special_button_pressed(self,ID):
        pass
    def on_special_button_released(self,ID):
        pass
    
    def on_message(self,multipart):
        pass
    
    def on_stop(self,ID):
        pass
    
    def on_pause(self,ID):
        pass
'''
Created on Jun 16, 2016

@author: joel
'''
from lm_soundboard_old.launchpad_mode import mode
from lm_soundboard_old.constants import *
from threading import Thread
# import wav_thread
import tkFileDialog
#from tkinter import filedialog
from Tkinter import Tk
from os.path import relpath
import copy
import swmixer


class Configmode(mode):
    '''
    classdocs
    '''
    
    #This list holds the colors each special button should be set to when returning to Default state

    def __init__(self, controller):
        '''
        Constructor
        '''
        self.controller = controller
        self.internal_mode = 'DEFAULT'
        
        self.bgm_default_options = {}
        self.bgm_default_options['filepath'] = ""
        self.bgm_default_options['loops'] = -1
        self.bgm_default_options['pausable'] = True
        self.bgm_default_options['volume'] = 1.0
        
        
        root = Tk()
        root.withdraw()
        
    
    def on_enter_mode(self):
        #Clear the local copies of the conf and grid
        self.conf = None
        self.grid = None
        #Load the current versions
        self.conf = self.controller.conf
        self.sound_path = self.conf["sound_path"]
        self.grid = self.conf['grid']
        self.selected = None
        #Light up all assigned buttons
        for ID in self.grid:
                self.controller.change_grid_color(ID,AMBER)
                
        #Light up the special buttons
        self.controller.change_special_color(hex(0x03),RED)
        
    def on_exit_mode(self):
        if self.selected:
            self.deselect()
    
    
    def on_grid_button_pressed(self,ID):
        
        if self.selected is None:
            #Select this button for changes
            
            if ID in self.grid:
                self.select(ID)
                #The selected button is already assigned, show that it is selected
                self.controller.change_grid_color(ID,AMBER_FLASHING)
            else:
                self.controller.change_grid_color(ID,GREEN_FLASHING)
                soundfile = tkFileDialog.askopenfilename(initialdir=self.sound_path,filetypes=[('Wave Audio file','*.wav'),
                                                                                              ('MP3 Audio file', '*mp3'),
                                                                                               ('All files', '*.*')])
                #Currently we are using relative paths, so make the path relative
                if soundfile:              
                    soundfile = relpath(soundfile,self.sound_path)
                    self.grid[ID] = {}
                    self.grid[ID]['filepath'] = soundfile
                    self.grid[ID]['loops'] = -1
                    self.grid[ID]['pausable'] = True
                    self.controller.change_grid_color(ID,AMBER)
                else:
                    self.controller.change_grid_color(ID,OFF)
                   
                
                
        else:
            #There already is a button selected
            if self.selected == ID:
                #Deselect
                self.deselect()
                #Update LED
                self.render_button(ID)
            else:
                #Prepare to move the selected button to the new ID
                temp = self.grid[self.selected]
                del(self.grid[self.selected])
                
                if ID in self.grid:
                    #The new position is already assigned, swap the two
                    self.grid[self.selected] = self.grid[ID]
                    
                self.grid[ID] = temp
                #Move selection to the new ID
                old_ID = self.selected
                self.selected = ID
                #Update both LEDs
                self.render_button(old_ID)
                self.render_button(ID)
                    
                
                
    def on_special_button_pressed(self, ID):
        btn_number = int(int(ID,0)/16)
        if btn_number == 0:
            if self.selected is not None:
                #first button (Play assigned sound)
#                 self.controller.send_message(['sample','RESTART'])
                self.sample_channel = self.sample_sound.play()
                self.controller.change_special_color(ID,GREEN)
                
            
    def on_special_button_released(self, ID):
        btn_number = int(int(ID,0)/16)
        if btn_number == 0:
            if self.selected is not None:
                #first button (Stop the sample sound)
#                 self.controller.send_message(['sample','STOP'])
                self.sample_channel.stop()
                self.sample_channel = None
                self.controller.change_special_color(ID,AMBER)
            
    def select(self,ID):
        if self.selected is not None:
            self.deselect()
        self.selected = ID
        #Get corresponding sound path
        soundfile = self.grid[self.selected]['filepath']
        path_to_wav = self.sound_path + soundfile
        self.sample_sound = swmixer.Sound(filename=path_to_wav)  
        #Now that the sample button is up, enable the sample button
        self.controller.change_special_color(hex(0x08),AMBER)
        
    def deselect(self):
        self.selected = None
        #Don't need the sample thread for this soundfile anymore
#         self.controller.send_message(['sample','DESTROY'])
        self.controller.change_special_color(hex(0x08),OFF)
        
    def render_button(self,ID):
        #Simple On/OFF rule for now, might get more complex later
        if ID == self.selected:
            color = AMBER_FLASHING
        elif ID in self.grid:
            color = AMBER
        else:
            color = OFF
        
        self.controller.change_grid_color(ID,color)
            

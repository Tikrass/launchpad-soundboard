'''
Created on Apr 3, 2016

@author: joel
'''

import rtmidi
#from rtmidi._rtmidi import MidiOut
#import zmq
#from threading import Thread
import lm_soundboard_old.constants as constants
from lm_soundboard_old.constants import numbers as led_numbers
from lm_soundboard_old.constants import GREEN, AMBER, RED, OFF

import random
import json
from lm_soundboard_old.constants import GREEN_FLASHING, RED_FLASHING, AMBER_FLASHING, FLASH_MODE_ON, FLASH_MODE_OFF, RESET_LEDS
from time import sleep
from lm_soundboard_old.soundboard_mode import Soundboardmode
from lm_soundboard_old.config_mode import Configmode
from lm_soundboard_old.delete_mode import Deletemode
#from tkinter import filedialog
from tkFileDialog import asksaveasfile, askopenfile
from os.path import split, abspath
import swmixer
import pyaudio


class Leds(object):
    '''
    classdocs
    '''  

    def __init__(self, path_to_conf="conf/blank.json", midiport=1):
        '''
        Constructor
        '''
        self.path_to_conf = path_to_conf
                
        
        #RTmidi init
        self.midi_out = rtmidi.MidiOut()
        self.midi_out.open_port(port=midiport, name="Launchpad_Leds")
        midi_out = self.midi_out
        
        self.midi_in = rtmidi.MidiIn()
        midi_in = self.midi_in
        midi_in.open_port(port=midiport, name="Note input")
        
        #Zmq init
        #self.ctx = zmq.Context()
        #self.sock = self.ctx.socket(zmq.ROUTER)  # @UndefinedVariable
        #sock = self.sock
        #sock.bind('inproc://launchpad')
        input_device_index=None
#         pya = pyaudio.PyAudio()
#         #Try to get the JACKd default output  
#         try :
#             input_device_index = pya.get_host_api_info_by_type(pyaudio.paJACK)['defaultOutputDevice']
#             
#         except:    
#             input_device_index = None
#         print input_device_index
#         #Kill pyaudio again, because swmixer will try to init it
#         pya.terminate()
        #Init and start swmixer
        swmixer.init(chunksize=10240,input_device_index=input_device_index)
        swmixer.start()
        
        midi_out.send_message(FLASH_MODE_ON)
        
        #load the test config
        self.conf = json.load(open(self.path_to_conf))
        
        self.modes = [None]*6        
        self.modes[0] = (Soundboardmode(self),GREEN)
        self.modes[1] = (Configmode(self),GREEN)
        self.modes[2] = (Deletemode(self),RED)

        self.curr_mode_index = 0        
        self.mode, color = self.modes[self.curr_mode_index]    
        self.mode.on_enter_mode()
        self.render_live()
        
        
        
        try:
            while True:
                
#                 try:
#                     multipart = sock.recv_multipart(zmq.NOBLOCK)  # @UndefinedVariable
#                     self.mode.on_message(multipart)
#                 except zmq.Again:
#                     #No message yet
#                     pass
                
                message = midi_in.get_message()
                
                if message != None:
                    #midi_in returns the actual midi message as first element
                    type , ID, velocity = message[0]
                    if type == 0x90:
                        if ID % 16 == 8:
                            ID = hex(ID)
                            #The ID belongs to a special button
                            if velocity:
                                self.mode.on_special_button_pressed(ID)
                            else:
                                self.mode.on_special_button_released(ID)
                        else:
                            ID = hex(ID)
                            #The ID belongs to a normal grid button
                            if velocity:
                                self.mode.on_grid_button_pressed(ID)
                            else:
                                self.mode.on_grid_button_released(ID)
                    elif type == 0xB0:
                        #The ID belongs to a live/automap button
                        btn_number = ID - 0x68
                        if velocity:
                            #self.mode.on_live_button_pressed(ID)
                            if(btn_number < 6):
                                self.change_mode(btn_number)
                            else:
                                #The rightmost buttons have special functions
                                if(btn_number == 6 ):
                                    self.open_conf()
                                if(btn_number == 7 ):
                                    self.save_conf()
                                
                        else:
                            #self.mode.on_live_button_released(ID)
                            pass
                    else:
                        print("Received invalid midi message")
                        print(message)
        except KeyboardInterrupt:
            self.shutdown()
                                 
#         
#         self.grid = dict()
#         grid = self.grid
#         
#         self.special = dict()
#         special = self.special
#         special[hex(0x08)] = (self.render_grid,AMBER)
#         #special[hex(0x18)] = (self.reload,AMBER)
#         
#         special[hex(0x38)] = (self.roll100_plus_plus,GREEN)
#         special[hex(0x48)] = (self.roll100_plus,GREEN)
#         special[hex(0x58)] = (self.roll100,AMBER)
#         special[hex(0x68)] = (self.roll100_minus,RED)
#         special[hex(0x78)] = (self.roll100_minus_minus,RED)
#         self.render_special()
#         
# 
#         self.conf_path = "conf/test.json"
#         self.load_grid_from_conf()
# 
#         self.start_special_sounds()
# 
#         
#         try:
#             while True:
#                 
#                 result = midi_in.get_message()
#                 
#                 if result != None:
#                 
#                     #midi_in returns the actual midi message as first element
#                     type , ID, velocity = result[0]
#                     if type == 0x90:
#                         if velocity:
#                             print result[0]
#                             #button was pressed
#                             
#                             
#                             if ID not in grid:
#                                 if ID in special:
#                                     #This button was assigned a special function, run that
#                                     (special[ID][0])()
#                                     print "special"                                    
#                                 else:
#                                     #Button not assigned, give visual feedback
#                                     midi_out.send_message([0x90 , int(ID,0) , RED])
#                             else:
#                                 if grid[ID]['state'] == 'PLAYING':
#                                     if grid[ID]['mode'] == 'LOOP':
#                                         #Do not repeat track when it finishes
#                                         grid[ID]['state'] = 'STOPPING'
#                                         #Give visual feedback, that the track is stopping
#                                         midi_out.send_message([0x90 , int(ID,0) , GREEN_FLASHING])
#                                     else:
#                                         #tell thread with corresponding id to pause
#                                         sock.send_multipart([ID,'PAUSE'])
#                                         #update status
#                                         grid[ID]['state'] = 'PAUSED'                            
#                                         #set the corresponding LED to amber
#                                         midi_out.send_message([0x90 , int(ID,0) , AMBER])
#                                 else:
#                                     #tell thread with corresponding id to play
#                                     sock.send_multipart([ID,'PLAY'])
#                                    
#                                     #update status
#                                     grid[ID]['state'] = 'PLAYING'
#                                     #set the corresponding LED to green
#                                     midi_out.send_message([0x90 , int(ID,0) , GREEN])
#                         else: 
#                             #Button was released
#                             if ID not in grid and ID not in special:
#                                 #An unassigned button was released, turn LED off again
#                                 midi_out.send_message([0x90 , int(ID,0) , OFF])
#                     
#                 try:    
#                     ID, msg = sock.recv_multipart(zmq.NOBLOCK)  # @UndefinedVariable
#                     print "Received message %s from thread %s \n" % (msg,ID)
#                     if msg == 'FINISHED':
#                         #Sound file finished playing
#                         if (grid[ID]['mode'] == 'LOOP' or grid[ID]['mode'] == 'LOOP_PAUSABLE' ) \
#                         and grid[ID]['state'] != 'STOPPING':
#                             #restart the file immediately
#                             sock.send_multipart([ID,'RESTART'])
#                         else:
#                             #update status                    
#                             grid[ID]['state'] = 'STOPPED'
#                             #set LED back to Amber
#                             midi_out.send_message([0x90,int(ID,0),AMBER])
#                 except zmq.Again:
#                     pass
#         except KeyboardInterrupt:
#             self.shutdown()
            
        
#    def add_button(self,ID,soundfile,mode='DEFAULT'):
#        
#         t1 = Thread(target=wav_thread.main,args=(self.sound_path + soundfile, self.ctx, ID))
#         t1.setDaemon(True)
#         #track play state and mode of the button
#         self.grid[ID] = {}        
#         self.grid[ID]['state'] = 'STOPPED'
#         self.grid[ID]['mode'] = mode
#         t1.start()
#         #Light up the corresponding LED in AMBER
#         self.midi_out.send_message([0x90 , ID , AMBER])
        
                
    def render_number(self, number, offset,color):
        
        pattern = led_numbers[number]
        #offset is the upper left corner led, shift the pattern there
        pattern = [x + offset for x in pattern]
        
        #Just for testing, send updates sequentially
        for led in pattern:
            self.midi_out.send_message([0x90,led,color])
    
        
    def render_percentile(self,value):
        
        if value == 1:
            color = GREEN
        elif value == 0:
            color = RED
        else:
            color = AMBER
        
        self.render_number(int(value/10), 0x00, color)
        self.render_number(value % 10, 0x35, color)
    
    def roll100(self):
        self.display_roll(random.randrange(0,100))
    
    def roll100_plus(self):
        roll = min(random.randrange(1,101),random.randrange(1,101))
        if roll == 100:
            roll = 0
        self.display_roll(roll)
        
    def roll100_plus_plus(self):
        roll = min(random.randrange(1,101),random.randrange(1,101),random.randrange(1,101))
        if roll == 100:
            roll = 0
        self.display_roll(roll)
        
    def roll100_minus(self):
        roll = max(random.randrange(1,101),random.randrange(1,101))
        if roll == 100:
            roll = 0
        self.display_roll(roll)
        
    def roll100_minus_minus(self):
        roll = max(random.randrange(1,101),random.randrange(1,101),random.randrange(1,101))
        if roll == 100:
            roll = 0
        self.display_roll(roll)
    
        
    def display_roll(self,roll):
        
        self.clear_grid()
        self.midi_out.send_message(FLASH_MODE_ON)
        #Stalling blinking "Dice rolling"
        self.render_number(8, 0x00, AMBER_FLASHING)
        self.render_number(8, 0x35, AMBER_FLASHING)
        #Give some time to blink
        sleep(3)
        #Clear the roll area
        self.clear_roll()
        #Display actual roll
        self.render_percentile(roll)
        
#         #Play special sounds for fumbles or crits
#         if roll == 00:
#             self.sock.send_multipart(['fumble','PLAY'])
#         elif roll == 01:
#             self.sock.send_multipart(['crit','PLAY'])
#         
#         #self.midi_out.send_message(FLASH_MODE_OFF)
        
    def render_grid(self):
        #double buffer this maybe?
        for ID in (16*x+y for x in range(8) for y in range(8)):
            if ID in self.grid:
                color = constants.color_map[self.grid[ID]['state']]
            else:
                color = OFF
            
            self.midi_out.send_message([0x90,ID,color])
            
    def render_special(self):
        for ID in range(0x08,0x88,0x10):
            if ID in self.special:
                func, color = self.special[ID]
                self.midi_out.send_message([0x90,ID,color])
                
    def render_live(self):
        for i in range(len(self.modes)):
            if self.modes[i] is not None:
                color = AMBER
            else: 
                color = OFF            
            self.change_live_color(i, color)
            
        #Mark the current mode
        mode_class, color = self.modes[self.curr_mode_index]
        self.change_live_color(self.curr_mode_index, color)
        #Light up the open and save buttons
        self.change_live_color(6, AMBER)
        self.change_live_color(7, AMBER)
            
    def clear_grid(self):
        self.midi_out.send_message([0xB0,0x0,0x0])
        self.render_special()
        
    def clear_roll(self):
        self.render_number(8, 0x00, OFF)
        self.render_number(8, 0x35, OFF)
        

    def save_conf(self):
        
        current_dir, current_file = split(abspath(self.path_to_conf))
        conf_file = asksaveasfile(initialdir=current_dir,initialfile=current_file)
        
        if conf_file:
            json.dump(self.conf,conf_file, sort_keys=True, indent=4)
            print("Wrote config to file")
        else:
            print("Failed to open file for writing")
            
    def open_conf(self):
        current_dir, current_file = split(abspath(self.path_to_conf))
        conf_file = askopenfile(initialdir=current_dir,initialfile=current_file)
        
        if conf_file:
            self.conf = json.load(conf_file)
            print('Loaded config from file "'+conf_file.name+'"')
            self.path_to_conf = conf_file.name
            #Exit and Re-enter current mode to force a conf reload
            self.mode.on_exit_mode()
            self.mode.on_enter_mode()
        else:
            print('Failed to load config from file ')
            #Reflect the error in the LED
            self.change_live_color(6, RED)
            sleep(1)
            self.change_live_color(6, AMBER)
                
    def shutdown(self):
        #Reset launchpad before terminating
        self.midi_out.send_message(RESET_LEDS)
        
        #Make the current thread cleanup
        #Todo: this should be a destroy/close function, when that is implemented
        self.mode.on_exit_mode()
        for channel in swmixer.gmixer_srcs:
            channel.stop()
        swmixer.quit()
        
#         for ID in self.grid:
#             #Tell all registered threads to terminate too                
#             self.sock.send_multipart([ID,'DESTROY'])
#         #Destroy fumble and crit
#         self.sock.send_multipart(['fumble','DESTROY'])
#         self.sock.send_multipart(['crit','DESTROY'])
        print('Terminating...')
        
        
    def reset_leds(self):
        #This clears all LED states but also resets Flash mode
        self.midi_out.send_message(RESET_LEDS)
        #Turn Flash mode back on
        self.midi_out.send_message(FLASH_MODE_ON)
        
    def start_special_sounds(self):
#         #Start extra threads which can play fumble and crit sounds
#         t = Thread(target=wav_thread.main, args=(self.sound_path + "fumble.wav", self.ctx, 'fumble', True))
#         t.setDaemon(True)
#         t.start()
#         t = Thread(target=wav_thread.main, args=(self.sound_path + "crit.wav", self.ctx, 'crit', True))
#         t.setDaemon(True)
#         t.start()

        pass
        
    def change_grid_color(self,ID,color):
        if int(ID,0) not in [x*16+y for x in range(8) for y in range(8)]:
            #TODO: raise Hell
            pass
        else:
            self.midi_out.send_message([0x90,int(ID,0),color])
     
    def change_special_color(self,ID,color):
        if int(ID,0) not in [x*16+8 for x in range(8) ]:
            #TODO: raise Hell
            pass
        else:
            self.midi_out.send_message([0x90,int(ID,0),color])
            
    def change_live_color(self,ID,color):
        self.midi_out.send_message([0xB0,ID+0x68,color])
                    
    def send_message(self,multipart):
        self.sock.send_multipart(multipart)
        
    def change_mode(self,index):
        if self.modes[index] is not None and index is not self.curr_mode_index:
            #change out of current mode
            self.mode.on_exit_mode()
            #self.change_live_color(self.curr_mode_index, AMBER)
            #Reset launchpad LEDs
            self.reset_leds()
            #Set the new mode, change into it and update the led color
            self.curr_mode_index = index
            self.mode, color = self.modes[index]
            self.render_live()
            self.mode.on_enter_mode()

    def enter_soundboard_mode(self):
        grid = self.grid
        special = self.special
        sock = self.sock
        midi_in = self.midi_in
        midi_out = self.midi_out
        
        
        while True:
                
                result = midi_in.get_message()
                
                if result != None:
                
                    #midi_in returns the actual midi message as first element
                    type , ID, velocity = result[0]
                    if type == 0xB0:
                        #A button on the top row was pressed
                        self.on_live_button_pressed(result[0])
                    
                    if type == 0x90:
                        if velocity:
                            print(result[0])
                            #button was pressed
                            
                            
                            if ID not in grid:
                                if ID in special:
                                    #This button was assigned a special function, run that
                                    (special[ID][0])()
                                    print("special" )                                   
                                else:
                                    #Button not assigned, give visual feedback
                                    midi_out.send_message([0x90 , int(ID,0) , RED])
                            else:
                                if grid[ID]['state'] == 'PLAYING':
                                    if grid[ID]['mode'] == 'LOOP':
                                        #Do not repeat track when it finishes
                                        grid[ID]['state'] = 'STOPPING'
                                        #Give visual feedback, that the track is stopping
                                        midi_out.send_message([0x90 , int(ID,0) , GREEN_FLASHING])
                                    else:
                                        #tell thread with corresponding id to pause
                                        sock.send_multipart([ID,'PAUSE'])
                                        #update status
                                        grid[ID]['state'] = 'PAUSED'                            
                                        #set the corresponding LED to amber
                                        midi_out.send_message([0x90 , int(ID,0) , AMBER])
                                else:
                                    #tell thread with corresponding id to play
                                    sock.send_multipart([ID,'PLAY'])
                                   
                                    #update status
                                    grid[ID]['state'] = 'PLAYING'
                                    #set the corresponding LED to green
                                    midi_out.send_message([0x90 , int(ID,0) , GREEN])
                        else: 
                            #Button was released
                            if ID not in grid and ID not in special:
                                #An unassigned button was released, turn LED off again
                                midi_out.send_message([0x90 , int(ID,0) , OFF])
                    
                try:    
                    ID, msg = sock.recv_multipart(zmq.NOBLOCK)  # @UndefinedVariable
                    print("Received message %s from thread %s \n" % (msg,ID))
                    if msg == 'FINISHED':
                        #Sound file finished playing
                        if (grid[ID]['mode'] == 'LOOP' or grid[ID]['mode'] == 'LOOP_PAUSABLE' ) \
                        and grid[ID]['state'] != 'STOPPING':
                            #restart the file immediately
                            sock.send_multipart([ID,'RESTART'])
                        else:
                            #update status                    
                            grid[ID]['state'] = 'STOPPED'
                            #set LED back to Amber
                            midi_out.send_message([0x90,int(ID,0),AMBER])
                except zmq.Again:
                    pass

'''
Created on Jan 18, 2017

@author: joel
'''
import swmixer
from lm_soundboard.constants import *
import threading
#from gnomevfs._gnomevfs import Volume
from time import sleep
from lm_soundboard.pausable_timer import PausableTimer

class Gridbutton(object):
    '''
    classdocs
    '''


    def __init__(self,ID,controller, filepath, samplerate=44100, volume = 1.0, loops=0, start_fadein=0.0, pausable=False, unpause_fadein=5.0, pause_fadeout=5.0, stop_fadeout=0.0):
        self.sound_path=controller.conf["sound_path"]
        
        self.ID = ID
        self.mode = controller
        self.rate = samplerate;
        self.start_fadein = start_fadein;
        self.stop_fadeout = stop_fadeout
        self.pausable = pausable
        self.unpause_fadein = unpause_fadein
        self.pause_fadeout = pause_fadeout
        self.soundobj = swmixer.Sound(self.sound_path+filepath)
        
        self.loops=loops
        self.volume = volume
        self.chan = None
        self.stop_timer = None
        
        
    def on_press(self):
        if self.chan is None or self.chan.done:
            if self.stop_fadeout > 0 :
                fadetime = self.stop_fadeout*self.rate
                length = self.soundobj.get_length()
                env = [[length-fadetime,self.volume],[length,0]]
            else:
                env = None
            self.chan = self.soundobj.play(volume=self.volume, fadein=self.start_fadein*self.rate,loops=self.loops,envelope=env)
            if self.loops > -1:
                #This is a button that will eventually stop on it's own
                length = self.soundobj.get_length()*(1+self.loops)
                playtime = (length / float(self.rate) )
                if swmixer.gstereo:
                    playtime /= 2
                    
                self.stop_timer = PausableTimer(playtime, lambda: self.mode.on_stop(self.ID))
                self.stop_timer.start()                
            return GREEN
        else:
            if self.pausable:
                if not self.chan.active:
                    if self.unpause_fadein > 0:
                        pos = self.chan.get_position()
                        fadetime=self.unpause_fadein*self.rate
                        #set fadein (needs to be done manually, because swmixer is a little broken
                        self.chan.env.extend([[pos,0.0],[pos+fadetime, self.volume]])
                    self.unpause()
                    return GREEN
                else:
                    #currently playing, so pause
                    if self.pause_fadeout > 0:
                        pos = self.chan.get_position()
                        fadetime = self.pause_fadeout*self.rate
                        #set fadeout (needs to be done manually, because swmixer is a little broken
                        self.chan.env.extend([[pos,self.chan.get_volume()],[pos+fadetime,0]])
                        t = threading.Timer(self.pause_fadeout,self.pause)
                        t.start()
                        return GREEN_FLASHING
                    else:
                        self.pause()
                    
            else:
                #Playing, non pausable, just stop and remove Channel
                
                #Pause_fadout is used for early stoppage and can be distinct from end fadeout
                if self.pause_fadeout > 0:
                    pos = self.chan.get_position()
                    fadetime = self.pause_fadeout*self.rate
                    #set fadeout (needs to be done manually, because swmixer is a little broken
                    self.chan.env.extend([[pos,self.chan.get_volume()],[pos+fadetime,0]])
                    t = threading.Timer(self.pause_fadeout,self.stop)
                    t.start()
                    return GREEN_FLASHING
                else:
                    self.stop()
            
       
    def stop(self):
        if self.chan is not None:
            self.chan.stop()
            self.chan = None
            
        if self.stop_timer != None:
            self.stop_timer.cancel()
            self.stop_timer = None
        self.mode.on_stop(self.ID)
        
    def pause(self):
        if self.chan is not None:
            self.chan.pause()
        self.mode.on_pause(self.ID)
        if self.stop_timer is not None:
            self.stop_timer.pause()
        
    def unpause(self):
        if self.chan is not None:
            self.chan.unpause()
        if self.stop_timer is not None:
            self.stop_timer.start()
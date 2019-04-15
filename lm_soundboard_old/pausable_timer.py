'''
Created on Jan 30, 2017

@author: joel
'''
from threading import Timer
import time

class PausableTimer(object):
    '''
    classdocs
    '''


    def __init__(self, time, f, args=[], kwargs={}):
        '''
        Constructor
        '''
        self.time = time
        self.f = f
        self.args = args
        self.kwargs = kwargs
        self.timer = Timer(self.time,self.f,self.args,self.kwargs) 
    def pause(self):
        self.timer.cancel()
        self.time -= (time.time() - self.time_started)
        self.timer = Timer(self.time,self.f,self.args,self.kwargs)
    def start(self):
        self.time_started = time.time()
        self.timer.start()
    def cancel(self):
        self.timer.cancel()
        
'''
Created on 30.09.2017

@author: boronaro, joel
'''

import sys
import launchpad_py as launchpad

class Controller(object):
    '''
    Controller responsible for the main loop and switching the loop.
    '''


    def __init__(self, conf=None):
        '''
        Constructor
        
        Keyword arguments:
        conf -- path to a config file (default None) 
        '''
        
        self.lp = launchpad.Launchpad()
'''
Created on Apr 4, 2016

@author: joel
'''
import wave
import pyaudio
import zmq


'''
A class representing a single button on the soundboard, which should be
run in its own thread. Use ZMQ inproc messages to play/pause/restart/stop
the track
'''


def main(path_to_wav, zmq_context, zmq_identity,fire_and_forget=False):

    #Setup Zmq socket
    context = zmq_context                
    sock = context.socket(zmq.DEALER)  # @UndefinedVariable These constants appear at runtime
    sock.setsockopt(zmq.IDENTITY,zmq_identity)  # @UndefinedVariable
    sock.connect('inproc://launchpad')
    
    
           
    
    chunk = 1024*10
    playing = False
     
    #open the wav file  
    f = wave.open(path_to_wav,"rb")
    #instantiate PyAudio  
    p = pyaudio.PyAudio()  
    #prepare a stream  
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                    channels = f.getnchannels(),  
                    rate = f.getframerate(),  
                    output = True)  
    
    #Main loop
    while True:
        #get message
        try:
            message = sock.recv_string(zmq.NOBLOCK)  # @UndefinedVariable
            if message == 'PLAY' or message == 'RESTART':
                if message == 'RESTART':
                    f.rewind()
                playing = True
                
            elif message == 'STOP' or message == 'PAUSE':
                if message == 'STOP':
                    f.rewind()
                playing = False
                
            elif message == 'DESTROY':
                stream.close()                
                f.close()                
                sock.disconnect('inproc://launchpad')
                sock.close()
                print('Thread was EXTERMINATEd')
                break
            
        except zmq.Again:
            #No new message from the controller, continue main loop
            if playing:
                data = f.readframes(chunk)
                if data != '':
                    stream.write(data)
                else:
                    #We reached end of stream, pause and rewind 
                    playing = False
                    f.rewind()
                    
                    if not fire_and_forget:
                        #The controller needs to know when this thread finishes
                        sock.send_string('FINISHED')
                    
        
        
                

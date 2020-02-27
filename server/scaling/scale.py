import math

class scale:
    
    def __init__(self):
        test = 'test'
    
    def calculateBuffer(self, registeredUsers, activeSessions, minimumContainers, activeContainers, challenge):
        
        buf = registeredUsers, activeSessions, minimumContainers, activeContainers, challenge
        
        buffer = activeContainers + ((0.2 * (activeSessions - activeContainers)) + (0.05 * (registeredUsers - activeSessions)))
        roundedBuffer = math.ceil(buffer)
        print("buffer = {0}, rounded up to nearest int = {1}".format(buffer, roundedBuffer))
        
        
        return roundedBuffer
    
        
    
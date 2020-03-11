import math
from django.db import models
from containers.models import Container
from users.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone 

class scale:
    
    
    def calculateBuffer(self, registeredUsers, activeSessions, minimumContainers, activeContainers, challenge):
        activeSessions = self.getActiveSessions()
        
        buf = registeredUsers, activeSessions, minimumContainers, activeContainers, challenge
        
        buffer = activeContainers + ((0.2 * (activeSessions - activeContainers)) + (0.05 * (registeredUsers - activeSessions)))
        roundedBuffer = math.ceil(buffer)
        print("buffer = {0}, rounded up to nearest int = {1}".format(buffer, roundedBuffer))
        
        
        return roundedBuffer
    
    def calculateAllBuffers(self):
        print('test')
        return   
    
    def getActiveSessions(self):
        try:
            sessions = Session.objects.filter(expire_date__gte=timezone.now())
            
            uid_list = []
            for session in sessions:
                data = session.get_decoded()
                auid = data.get('_auth_user_id', None)
                if auid not in uid_list:
                    uid_list.append(auid)
                    
            return uid_list
                    
        except Exception as ex:
            raise(ex)
            
    def getRegisteredUsers(self):
        try:
            registeredUsers = User.objects.count()
        except Exception as ex:
            print(ex)
    
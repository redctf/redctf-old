from scale import scale
from users.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone

s = scale()

# example data - no need for separate file - will eventually just query docker to see what values are available. 
challengeID = 3
registeredUsers = 10
activeSessions = 10
activeContainers = 10
minimumContainers = 2

try:
    buf = s.calculateBuffer(registeredUsers, activeSessions, minimumContainers, activeContainers, challengeID)
    
except Exception as ex:
    print(ex)

if buf == activeContainers:
    print("buffer ({0}) is exactly the # of active contianers({1})".format(buf, activeContainers))
          
elif buf < activeContainers:
    print("calculated buffer ({0}) is less than the # of active contianers({1}) \n\r{2} containers required (-1 to account for rounding calculation)".format(buf, activeContainers, buf - activeContainers + 1)) # +1 to account for rounding up on buffer calculation but still erring on the side of caution for removing containers
          
elif buf > activeContainers:
    print("calculated buffer ({0}) is more than the # of active contianers({1}) \n\r{2} containers required".format(buf, activeContainers, buf - activeContainers))
    
else:
    print("idk how we got here")
from exampleData import data as d
from scale import *

s = scale()

try:
    buf = s.calculateBuffer(d.registeredUsers, d.activeSessions, d.minimumContainers, d.activeContainers, d.challenge)
    
except Exception as ex:
    print(ex)

if buf == d.activeContainers:
    print("buffer ({0}) is exactly the # of active contianers({1})".format(buf, d.activeContainers))
          
elif buf < d.activeContainers:
    print("calculated buffer ({0}) is less than the # of active contianers({1}) \n\r{2} containers required".format(buf, d.activeContainers, buf - d.activeContainers + 1)) # +1 to account for rounding up on buffer calculation but still erring on the side of caution for removing containers
          
elif buf > d.activeContainers:
    print("calculated buffer ({0}) is more than the # of active contianers({1}) \n\r{2} containers required".format(buf, d.activeContainers, buf - d.activeContainers))
    
else:
    print("idk how we got here")
import json
import pprint

from dockerAPI import dockerAPI 
d = dockerAPI()

pp = pprint.PrettyPrinter(indent=4)
retcode = 0

path = "/"
filename = "./dockerLint/dockerfile-bad"
dockerfile = 'dockerfile-bad'
rulesfile = "rules.yaml"
volume = '/home/nate/redctf/dockerLint'
debug = True
print("##################\nJSON:")

r = d.parseDockerfile(filename)

pp.pprint(r)
print("##################\nLinter debug = False")


try:
    r_lint = d.lintDockerFile(dockerfile, rulesfile, volume, False)
    print(r_lint)
    
except Exception as ex:
    print(ex)
    retcode = 1

print("##################\nLinter debug = True")   

try:    
    r_lint_debug = d.lintDockerFile(dockerfile, rulesfile, volume, debug)
    print(r_lint_debug)
except Exception as ex:
    print(ex)
    retcode = 1
    
exit(retcode)

import json
import pprint

from dockerfileParse import dockerAPI 
d = dockerAPI()

pp = pprint.PrettyPrinter(indent=4)


path = "/"
filename = "./dockerLint/dockerfile"
rulesfile = "./dockerLint/rules.yaml"
print("##################")

r = d.parseDockerfile(filename)

pp.pprint(r)
print("##################")
# print("JSON:\n{0}".format(r))
# print("##################")

try:
    r_lint = d.lintDockerFile(filename, rulesfile)
    print(r_lint)
except Exception as ex:
    print(ex)
    
exit(0)

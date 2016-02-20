import click
import generate
import os

'''
    ocsm init comes here! 
'''
def initialize():
    add_gitignore()
    status = generate.generate()
    if status["code"] ==0:
        print "ERROR: could not generate config.oscm, " + str(status.error_desc)
        return 0
    #oscm_prompt.prompt()
    return 1

def add_gitignore():
    p = os.path.join(os.getcwd(),".gitignore")
    fp = open(p,"w")
    fp.write("*/")
    fp.close()

if __name__ == '__main__':
    print str(init())
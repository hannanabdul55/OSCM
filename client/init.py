import click
import generate
import oscm_prompt


'''
    ocsm init comes here! 
'''
def init():
    status = generate.generate()
    if status.code ==0:
        print "ERROR: could not generate config.oscm, " + str(status.error_desc)
        return 0
    oscm_prompt.prompt()
    return 1
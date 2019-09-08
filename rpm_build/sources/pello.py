#!/usr/bin/env python3
#
################################################################################
#developer: pushtakio
#purpose: to say hello
#date: 08/09/2019
#ver: 1.0.0
################################################################################

#### imports
import os
import sys
import getpass
import argparse
import time
####Variables :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
line="#######################################################################"
user=getpass.getuser()
msg_root="This Tool Can Not Be Used With $EUID User"
msg_permssions="Please Decrease your level to regular user"
####functions /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/

def deco(user):
    pre_=line
    post=line

    print(pre_+"\n"+"# hello "+ user+"\n"+post)

####
#Main - _- _- _- _- _- _- _- _- _- _- _- _- _- _- _- _- _- _- _- _- _- _- _- _- _
####
if __name__ == "__main__":
    if os.getuid() == 0:
        print("\n"+msg_root)
        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
        sys.exit(1)
    else:
        deco(user)
        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
        sys.exit()

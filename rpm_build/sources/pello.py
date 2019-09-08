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
import getpass
import argparse

####Variables :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
line="#######################################################################"
user=getpass.getuser()
msg_root="This Tool Can Not Be Used With $EUID User"
msg_permssions="Please Decrease your level to regular user"
####functions /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/

def deco(user):
    pre_=line
    post=line

    print(pre+"\n"+"# hello "+ user+"\n"+post)




####
if __main__ == "__name__":
    deco(user)

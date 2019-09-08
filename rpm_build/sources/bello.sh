#!/usr/bin/env bash
#
################################################################################
#developer: pushtakio
#purpose: to say hello
#date: 08/09/2019
#ver: 1.0.14
################################################################################


####Variables::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
_time=2
line="#########################################################################"
msg_root="This Tool Can Not Be Used With $EUID User"
msg_permssions="Please Decrease your level to regular user"
####Functions /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/
deco(){
  pre="$line"
  post="$line"
  printf "\n$pre\n#%s\n$post\n" "$@"
}

hello(){
 user=$1
 sleep 1
 if [[ "$@" == "" ]];then
   deco "Hello $USER"
else
  deco "Hello $@"
fi
}


####
#Main _ -_ -_ -_ -_ -_ -_ -_ -_ -_ -_ -_ -_ -_ -_ -_ -_ -_ -_ -_ -_ -_ -_ -_ -
####

if [[ $EUID == "0" ]];then
  clear
  deco "$msg_root"
  sleep $_time
  clear
  deco "$msg_permssions"
  sleep $_time
  clear
  exit 1
else
  clear
    hello "$@"
      sleep $_time
  clear
fi

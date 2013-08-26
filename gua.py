#! /usr/bin/env python3.3
# -*- code:utf-8 -*-

import os

# record disks' serials into file '.atm_*'.
os.system("sudo fdisk -l|grep -o /dev/sd\[b-z\]\[1-9\]|grep -o \[b-z\]\[1-9\]"
            ">> /tmp/.atm_all")
os.system("sudo fdisk -l|grep /dev/sd\[b-z\]\[1-9\]|grep -o \[NF\]\[TA\]\[FT\]\[S3\]2\*"
            ">> /tmp/.atm_all_type")
os.system("df|grep -o /dev/sd\[b-z\]\[1-9\]|grep -o \[b-z\]\[1-9\]"
            ">> /tmp/.atm_m")

file_handle_all = open("/tmp/.atm_all", 'r') 
file_handle_all_type = open('/tmp/.atm_all_type', 'r') 
file_handle_m = open('/tmp/.atm_m', 'r')

# read this data into memory now.
file_list_all = file_handle_all.readlines()
file_list_m = file_handle_m.readlines()
types = file_handle_all_type.readlines()

count = 0
index = 0
operands = []
for la in file_list_all:
    mounted = False
    for lm in file_list_m:
        if lm == la:
            mounted = True
            break
    if not mounted:
        count += 1
        operands.append("sd"+la[:-1])
        print(str(count)+". mount /dev/"+operands[count-1]+" on ~/media/"+
                operands[count-1]+"/ type:"+types[index])
        # make directory
        if not os.path.exists("/home/auchan/media/"+operands[count-1]):
            os.system("mkdir ~/media/"+operands[count-1])

        # must have installed ntfs-3g
        if types[index][:-1] == 'NTFS':
            os.system("sudo ntfs-3g /dev/"+operands[count-1]+" ~/media/"+operands[count-1])
        elif types[index][:-1] == 'FAT32':
            os.system("sudo mount -o umask=0 /dev/"+operands[count-1]+" ~/media/"+operands[count-1])
    index += 1


# close file
file_handle_all.close()
file_handle_m.close()
 
# delete temporary files
os.system("rm /tmp/.atm_all /tmp/.atm_all_type /tmp/.atm_m")

# -*- coding: utf-8 -*-
"""
Created on Tue May 24 22:26:57 2022

@author: lapcell
"""

from flask import Flask,render_template,request
import ipaddress
import subprocess
import re
import socket


listOfIPs = []
UpIPs = []
downIPs = [] 
scanner=[]

def scanIPS(IP1, IP2):
    listOfIPs = []
    UpIPs = [] 
    downIPs = [] 
    macAddress = []
    
    ip1 = int(ipaddress.IPv4Address(IP1))
    ip2 = int(ipaddress.IPv4Address(IP2))

    terminal_output1 = ""
    terminal_output2 = ""

    for ip in range(ip1, ip2 + 1):
        Process = subprocess.getoutput("ping -n 1 " + str(ipaddress.IPv4Address(ip)))
        terminal_output1 += Process
        String_Needed = re.compile(r"TTL=")
        term = String_Needed.search(terminal_output1)
        try:
            if term.group() == "TTL=":
                listOfIPs.append("HOST " + str(ipaddress.IPv4Address(ip)) + " IS UP")
                UpIPs.append(str(ipaddress.IPv4Address(ip)))
                Process2 = subprocess.getoutput("arp -a " + str(ipaddress.IPv4Address(ip)))
                terminal_output2 += Process2
                out = terminal_output2.split("\n")
                dash = out[3].find('-')
                MAC_ADD = out[3][dash-2:dash+15]
                print(MAC_ADD)
                macAddress.append(MAC_ADD)
        except:
            listOfIPs.append("HOST " + str(ipaddress.IPv4Address(ip)) + " IS DOWN")
            downIPs.append(str(ipaddress.IPv4Address(ip)))

        terminal_output1 = ""
        terminal_output2 = ""
    return listOfIPs,UpIPs,downIPs,macAddress



def portscanner(IP):
    for port in range(1,500):
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.settimeout(0.1)
        result= s.connect_ex((IP,port))
        if result==0:
            x="Port" +" " +str(port) +" "+ "is open"
            scanner.append(x)
        else:
            continue
            s.close()
    return scanner
    
    
app=Flask(__name__)





@app.route('/',methods=["GET","POST"])
def hello(): 
    scanner=[]
    list1=[]
    list2=[]
    list3=[]
    list4=[]
    
    if request.method == "POST":
        req=request.form
        firstIP=req["IP1"]
        lastIP=req["IP2"] 
        list1,list2,list3,list4=scanIPS(firstIP,lastIP)
        print(list4)
        for i in range(len(list2)):
            scanner=portscanner(list2[i])
            print(f"Opened ports of IP {list2[i]} are: {scanner}")   
            
        
    return render_template("scanner.html",arg=list1,UpIPs=list2,ports=scanner,macaddress=list4)


if __name__== "__main__":
    app.run(port=6096)
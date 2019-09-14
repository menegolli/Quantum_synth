# from flask import Flask,render_template
from qiskit import *
import numpy as np
import operator
import socket
import argparse
import random
import time
import logging
from backends_select import ChooseBackEnd
from SuperpositionGates import *
from RenormalizeProbability import *

from pythonosc import udp_client


# UDP_IP_SERVER="192.168.14.152"
#UDP_IP_SERVER="10.17.0.48"
#UDP_IP_SERVER="192.168.1.150"
UDP_IP_SERVER="127.0.0.1"
UDP_PORT_SERVER=7001

# global functions
log = logging.getLogger('udp_server')



def sender(results,name):
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default=UDP_IP_SERVER,
      help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=7000,
      help="The port the OSC server is listening on")
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.ip, args.port)
    # for k in sorted(results):
    #     print(k, results[k])
    #     client.send_message(k, results[k])
    client.send_message(name, results)
    return True


def server(host='0.0.0.0', port=UDP_PORT_SERVER):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    log.info("Listening on udp %s:%s" % (host, port))
    s.bind((host, port))
    return s

def grover4(target, backendType, RealDeviceName,noisePresent=False,number=12):
    listForMusic = GroverSequence(target=target, initialLength=4, backendType=backendType, RealDeviceName=RealDeviceName, noisePresent=noisePresent)

    message = ""
    for k in listForMusic:
        # ii = 0
        print(k)
        if number== 12:
            k=RedistributeCell(k)
        print(k)
        for l in k:
            message = message + str(l) + " "
            # ii = ii + 1
            # if ii == 12:
            #     print(ii)
            #     break
    print(message)
    sender(results=message, name="grover")

def hadamard(backendType, RealDeviceName, noisePresent,numberShots,number=12):
    circuit=QuantumCircuit(4,4)
    Hadamard(circuit, listOfQubits=range(4))
    listForMusic = ChooseBackEnd(circuit, backendType=backendType, qubitsToBeMeasured=range(4), numberShots=numberShots, noisePresent=noisePresent, RealDeviceName=RealDeviceName,number=number)
    print(listForMusic)

    if number==12:
        listForMusic = RedistributeCell(listForMusic)

    print(listForMusic)
    sender(results=listForMusic, name="prob")

    del(circuit)

def Bell(backendType, RealDeviceName, noisePresent,numberShots,number=12):
    circuit=QuantumCircuit(4,4)
    BellStateGenerationTwoQubits(circuit)
    listForMusic = ChooseBackEnd(circuit, backendType=backendType, qubitsToBeMeasured=range(4), numberShots=numberShots, noisePresent=noisePresent, RealDeviceName=RealDeviceName)
    print(listForMusic)
    if number==12:
        listForMusic = RedistributeCell(listForMusic)
    print(listForMusic)
    sender(results=listForMusic, name="prob")
    del(circuit)

def SeperPosition(backendType, RealDeviceName, noisePresent,numberShots,number=12,notes=range(4)):
    circuit=QuantumCircuit(4,4)
    ChooseEqualSuperposition(circuit,states=notes)#we have to check togather
    listForMusic = ChooseBackEnd(circuit, backendType=backendType, qubitsToBeMeasured=range(4), numberShots=numberShots, noisePresent=noisePresent, RealDeviceName=RealDeviceName)
    print(listForMusic)
    if number==12:
        listForMusic = RedistributeCell(listForMusic)
    print(listForMusic)
    sender(results=listForMusic, name="prob")
    del(circuit)

if __name__ == '__main__':
    # app.run()
  # test=hello_world()
    FORMAT_CONS = '%(asctime)s %(name)-12s %(levelname)8s\t%(message)s'
    logging.basicConfig(level=logging.DEBUG, format=FORMAT_CONS)
    # music = QuantumCircuit(4,4)
    # ['qasm_simulator', 'ibmq_16_melbourne', 'ChooseEqualSuperposition', '1936', '0']
    s=server()

    while True:
        while True:
            (mystr, addr) = s.recvfrom(128*1024)
            print("Message from MAX:{}".format(mystr))
            mystr=str(mystr)
            mystr = mystr.split("'")
            mystr = mystr[1]
            mystr = mystr.split("stop")
            mystr = mystr[0]
            mystr = mystr.split("run")
            mystr = mystr[1]
            mystr=mystr.strip()
            mystr = mystr.split(" ")
            print(mystr)
            #targ=format(3,'#06b')[2:]
            targ=mystr[6]
            targ="0"*(4-len(targ))+targ

            print(targ)
            # listForMusic = ChooseBackEnd(music, backendType=mystr[0], qubitsToBeMeasured=range(4), numberShots=int(mystr[3]), noisePresent=True, RealDeviceName=mystr[1])
            if mystr[4]=='1':
                noise=True
            elif mystr[4]=='1':
                noise=False
            else:
                noise=False
            print(int(mystr[6],2))
            if mystr[2]=="Hadamard":
                hadamard(backendType=mystr[0], RealDeviceName=mystr[1], noisePresent=noise,numberShots=int(mystr[3]),number=int(mystr[5]))
            elif mystr[2]=="BellStateGenerationTwoQubits":
                 Bell(backendType=mystr[0], RealDeviceName=mystr[1], noisePresent=noise,numberShots=int(mystr[3]),number=int(mystr[5]))
            elif mystr[2]=="ChooseEqualSuperposition":
                SeperPosition(backendType=mystr[0], RealDeviceName=mystr[1], noisePresent=noise,numberShots=int(mystr[3]),number=int(mystr[5]))
            elif mystr[2]=="Grover":
                grover4(target=targ, backendType=mystr[0], RealDeviceName=mystr[1], noisePresent=noise,number=int(mystr[5]))
            else:
                print("Command Not defined")





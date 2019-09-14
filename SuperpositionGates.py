#!/usr/bin/env python
# coding: utf-8

# In[44]:


from qiskit import *
import numpy as np
#import NewBackends
import random
import sys
from backends_select import ChooseBackEnd


# In[64]:


def GenerateCircuitSingleNote(circuit, note_id):
    '''
    Adds to the circuit the gates to measure a given note.
    '''
    if (note_id >= 12):
        sys.exit("Note must be an integer smaller than 11 and larger (or equal) to 0.")
    bitstring = str(bin(note_id)[2:])
    bitstring = "0"*(4-len(bitstring))+bitstring
    for i in range(len(bitstring)):
        if bitstring[len(bitstring)-1-i] == "1":
            circuit.x(i)

def BellStateGenerationTwoQubits(quantumCircuit, firstQubit=0, secondQubit=1, specificEntangledState="Phi"):
    if specificEntangledState == "Phi":
        quantumCircuit.h(firstQubit)
        quantumCircuit.cx(firstQubit, secondQubit)
    elif specificEntangledState == "Psi":
        quantumCircuit.h(firstQubit)
        quantumCircuit.x(secondQubit)
        quantumCircuit.cx(firstQubit, secondQubit)

def ChooseEqualSuperposition(quantumCircuit, states):
    desiredVector = np.zeros(2**quantumCircuit.n_qubits)
    flag = 1
    for k in states:
        if 0 <= k <= 11:
            desiredVector[k] = 1/np.sqrt(len(states))
            flag = flag*1
        else:
            flag = flag*0
    if flag == 1:
        quantumCircuit.initialize(desiredVector, range(4))

def ChooseEqualSuperpositionRandom(quantumCircuit):
    randomNumberOfNotes = np.random.randint(2,13)
    listModes = list(range(12))
    listToSuperimpose = []
    for i in range(randomNumberOfNotes):
        tmp = random.choice(listModes)
        listToSuperimpose.append(tmp)
        listModes.remove(tmp)
    ChooseEqualSuperposition(quantumCircuit, listToSuperimpose)
            
def Hadamard(quantumCircuit, listOfQubits):
    for k in listOfQubits:
        if 0 <= k <= quantumCircuit.n_qubits:
            quantumCircuit.h(k)
            
def RandomRotation(quantumCircuit):
    for k in range(quantumCircuit.n_qubits):
        quantumCircuit.u3(q=k, theta = np.random.random()*2*np.pi, phi = np.random.random()*np.pi, lam = np.random.random()*np.pi)
        
def __multiplecz(quantumCircuit, target, initialLength):
    quantumCircuit.ccx(0,1, initialLength)
    for k in range(2, initialLength-1):
        quantumCircuit.ccx(k, initialLength+k-2, initialLength+k-1)
    quantumCircuit.cz(quantumCircuit.n_qubits-1, initialLength-1)
    for k in reversed(range(2, initialLength-1)):
        quantumCircuit.ccx(k, initialLength+k-2, initialLength+k-1)
    quantumCircuit.ccx(0,1, initialLength)
    
def Grover(quantumCircuit, target, initialLength):
    for k in range(initialLength):
        quantumCircuit.h(k)
    ancillaQubit = QuantumRegister(2)
    quantumCircuit.add_register(ancillaQubit)
    for n in range(int(np.round(np.pi/4*np.sqrt(2**initialLength)))):
        
        for singleBit in range(initialLength):
            if target[initialLength-singleBit-1] == '0':
                quantumCircuit.x(singleBit)
        __multiplecz(quantumCircuit, target, initialLength)
        for singleBit in range(initialLength):
            if target[initialLength-singleBit-1] == '0':
                quantumCircuit.x(singleBit)
                
        for qubit in range(initialLength):
            quantumCircuit.h(qubit)
            quantumCircuit.x(qubit)
        __multiplecz(quantumCircuit, target, initialLength)
        for qubit in range(initialLength):
            quantumCircuit.x(qubit)
            quantumCircuit.h(qubit)


def AmplitudeAmplification(quantumCircuit, target, initialLength, numIterations):
    for k in range(initialLength):
        quantumCircuit.h(k)
    ancillaQubit = QuantumRegister(2)
    quantumCircuit.add_register(ancillaQubit)
    for n in range(numIterations):
        for singleBit in range(initialLength):
            if target[initialLength - singleBit - 1] == '0':
                quantumCircuit.x(singleBit)
        __multiplecz(quantumCircuit, target, initialLength)
        for singleBit in range(initialLength):
            if target[initialLength - singleBit - 1] == '0':
                quantumCircuit.x(singleBit)

        for qubit in range(initialLength):
            quantumCircuit.h(qubit)
            quantumCircuit.x(qubit)
        __multiplecz(quantumCircuit, target, initialLength)
        for qubit in range(initialLength):
            quantumCircuit.x(qubit)
            quantumCircuit.h(qubit)

def HalfFilledSuperposition(quantumCircuit, number):
    desiredVector=np.zeros(16)
    for k in range(number//2):
        desiredVector[k] = 1./np.sqrt(number/2.)
    quantumCircuit.initialize(desiredVector, range(4))



def GroverSequence(target, initialLength,backendType,RealDeviceName,noisePresent):
    iterations = []
    for k in range(4):
        temporaryQuantumCircuit = QuantumCircuit(initialLength, initialLength)
        AmplitudeAmplification(temporaryQuantumCircuit, target, initialLength, k)
        print(target)
        #             listForMusic = ChooseBackEnd(music, backendType=mystr[0], qubitsToBeMeasured=range(4),
        #             numberShots=int(mystr[3]), noisePresent=True, RealDeviceName=mystr[1])

        iterations.append(ChooseBackEnd(quantumCircuit=temporaryQuantumCircuit, noisePresent=noisePresent,backendType=backendType,qubitsToBeMeasured=range(4),RealDeviceName=RealDeviceName))
        # ChooseBackEnd(quantumCircuit=temporaryQuantumCircuit, noisePresent=True,backendType=backendType,qubitsToBeMeasured=range(4),RealDeviceName=RealDeviceName)
        del (temporaryQuantumCircuit)

    return iterations


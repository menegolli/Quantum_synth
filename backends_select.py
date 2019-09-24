#!/usr/bin/env python
# coding: utf-8

# In[1]:


from qiskit import *
import numpy as np
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute
from qiskit import Aer, IBMQ  # import the Aer and IBMQ providers
from qiskit.providers.aer import noise  # import Aer noise models
from qiskit.tools.monitor import job_monitor
from RenormalizeProbability import *



# In[7]:


def ChooseBackEnd(quantumCircuit, backendType="statevector_simulator", qubitsToBeMeasured=range(4), numberShots=4096, noisePresent=False, RealDeviceName="ibmq_ourense",number=12):

    if backendType == "statevector_simulator":
        backend = Aer.get_backend('statevector_simulator')
        result = execute(quantumCircuit, backend).result()
        probabilityVectors = np.square(np.absolute(result.get_statevector()))
        listForMusic = []
        for k in range(2**len(qubitsToBeMeasured)):
            listForMusic.append("%.3f" % (probabilityVectors[k]))

    elif backendType == "qasm_simulator":
        if noisePresent == False:
            # no noise
            quantumCircuit.measure(qubitsToBeMeasured, qubitsToBeMeasured)
            print(qubitsToBeMeasured)

            backend = Aer.get_backend('qasm_simulator')
            result = execute(quantumCircuit, backend, shots=numberShots).result()
            counts = result.get_counts()
            listForMusic = []
            for i in range(2**len(qubitsToBeMeasured)):
                bitstring = str(bin(i)[2:])
                bitstring = "0"*(4-len(bitstring))+bitstring
                if bitstring in counts.keys():
                    listForMusic.append("%.3f" % (counts[bitstring]/float(numberShots)))
                else:
                    listForMusic.append("0.000")
        else:
            print(qubitsToBeMeasured)
            quantumCircuit.measure(qubitsToBeMeasured,qubitsToBeMeasured)
            provider=IBMQ.save_account('XXX-YOUR-TOKEN')
            # simulate noise of a real device
            IBMQ.load_account()
            IBMQ.providers()


            device = IBMQ.get_provider(hub='ibm-q', group='open', project='main').get_backend(RealDeviceName)
            properties = device.properties()
            coupling_map = device.configuration().coupling_map

            # Generate an Aer noise model for device
            noise_model = noise.device.basic_device_noise_model(properties)
            basis_gates = noise_model.basis_gates


            # Perform noisy simulation
            backend = Aer.get_backend('qasm_simulator')
            job_sim = execute(quantumCircuit, backend,
                              coupling_map=coupling_map,
                              noise_model=noise_model,
                              basis_gates=basis_gates)
            result = job_sim.result()

            counts = result.get_counts()
            listForMusic = []
            for i in range(2**len(qubitsToBeMeasured)):
                bitstring = str(bin(i)[2:])
                bitstring = "0"*(4-len(bitstring))+bitstring
                if bitstring in counts.keys():
                    listForMusic.append("%.3f" % (counts[bitstring]/float(numberShots)))
                else:
                    listForMusic.append("0.000")
    elif backendType == "real_device":
        # real device
        quantumCircuit.measure(qubitsToBeMeasured,qubitsToBeMeasured)
        provider=IBMQ.save_account('XXX-YOUR-TOKEN')
        # simulate noise of a real device
        IBMQ.load_account()
        IBMQ.providers()


        device = IBMQ.get_provider(hub='ibm-q', group='open', project='main').get_backend(RealDeviceName)
        job_exp = execute(quantumCircuit, backend=device)

        job_monitor(job_exp)

        result = job_exp.result()

        counts = result.get_counts()
        listForMusic = []
        for i in range(2**len(qubitsToBeMeasured)):
            bitstring = str(bin(i)[2:])
            bitstring = "0"*(4-len(bitstring))+bitstring
            if bitstring in counts.keys():
                listForMusic.append(" %.3f" % (counts[bitstring]/float(numberShots)))
            else:
                listForMusic.append("0.000")


    return listForMusic


# In[70]:
if __name__ == "__main__":
    # qc = QuantumCircuit(2,2)
    # qc.h(0)
    # qc.x(1)
    #
    # res = ChooseBackEnd(qc,"qasm_simulator",200)


    # In[8]:


    music = QuantumCircuit(4,4)

    desired_vector = np.zeros(np.power(2,4))

    desired_vector[1] = 1 / np.sqrt(3)
    desired_vector[3] = 1/np.sqrt(3)
    desired_vector[10] = 1/np.sqrt(3)

    music.initialize(desired_vector, range(4))

    listForMusic= ChooseBackEnd(music,backendType="statevector_simulator",qubitsToBeMeasured=range(4),
                                numberShots=4096, noisePresent=True, RealDeviceName="ibmq_16_melbourne")
    print(listForMusic)


# In[ ]:

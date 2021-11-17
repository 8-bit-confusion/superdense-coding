#!/usr/bin/env python
# coding: utf-8

import qiskit

# print(qiskit.__version__)
qiskit.IBMQ.load_account()

ascii_subset = 'abcdefghijklmnopqrstuvwxyz,. "!?'

def get_binary(char):
    int_vers = ascii_subset.find(char)
    bin_vers = format(int_vers, 'b')
    while len(bin_vers) < 5:
        bin_vers = '0' + bin_vers
    return bin_vers

def initialize(circuit):
    circuit.h(0)
    circuit.h(1)
    circuit.cx(0, 3)
    circuit.cx(1, 2)
    circuit.cx(2, 4)

def encode(char, circuit):
    binary = get_binary(char)
    if binary[0] == '1':
        circuit.z(0)
    if binary[1] == '1':
        circuit.z(1)
    if binary[2] == '1':
        circuit.x(1)
    if binary[3] == '1':
        circuit.x(0)
    if binary[4] == '1':
        circuit.x(1)
        circuit.x(2)

def delay(circuit):
    for i in range(16):
        circuit.i(0)
        circuit.i(1)
        circuit.i(2)

def decode(circuit):
    circuit.cx(2, 4)
    circuit.cx(1, 2)
    circuit.cx(0, 3)
    circuit.h(1)
    circuit.h(0)

def measure(circuit, qr, cr):
    circuit.measure(qr, cr)

def reset(circuit):
    circuit.reset(0)
    circuit.reset(1)
    circuit.reset(2)
    circuit.reset(3)
    circuit.reset(4)

def get_char(result_counts):
    result_keys = list(result_counts)
    results = [result_counts[i] for i in result_keys]
    
    max_val = max(results)
    index = results.index(max_val)
    key = result_keys[index]
    
    key = key[::-1]
    
    int_vers = int(key, 2)
    char = ascii_subset[int_vers]
    
    return char

def evaluate_error(send, receive):
    total = len(send)
    same = total
    for i in range(len(send)):
        if send[i] == receive[i]:
            same -= 1
    
    return same/total

def run(circuit, nshots, system = 'ibmq_manila'):
    provider = qiskit.IBMQ.get_provider('ibm-q')
    qcomp = provider.get_backend(system)
    
    print('System Status: '+qcomp.status().status_msg)
    
    job = qiskit.execute(circuit, backend=qcomp, shots = nshots)
    qiskit.tools.monitor.job_monitor(job)
    
    result = job.result()
    return result

if __name__ == "__main__":
    qr = qiskit.QuantumRegister(5)
    cr = qiskit.ClassicalRegister(5)
    circuit = qiskit.QuantumCircuit(qr,cr)
    
    provider = qiskit.IBMQ.get_provider('ibm-q')
    qcomp = provider.get_backend('ibmq_bogota')
    
    send_char = '!'
    
    initialize(circuit)
    encode(send_char, circuit)
    delay(circuit)
    decode(circuit)
    measure(circuit, qr, cr)
    
    # print(circuit)
    
    job = qiskit.execute(circuit, backend=qcomp)
    qiskit.tools.monitor.job_monitor(job)
    
    result = job.result()
    # print(result.get_counts(circuit))
    
    receive_char = get_char(result.get_counts(circuit))
    print(send_char, '->', receive_char)
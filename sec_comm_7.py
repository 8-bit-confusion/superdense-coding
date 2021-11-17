# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 09:53:54 2021

@author: 831995
"""

import qiskit

qiskit.IBMQ.load_account()

def get_binary(char: str) -> str:
    int_vers = ord(char)
    bin_vers = format(int_vers, 'b')
    while len(bin_vers) < 7:
        bin_vers = '0' + bin_vers
    # print(char, chr(int(bin_vers, 2)))
    return bin_vers

def initialize(circuit: qiskit.circuit.QuantumCircuit, n: int) -> None:
    if n == 5:
        circuit.h(0)
        circuit.h(1)
        circuit.cx(0, 3)
        circuit.cx(1, 2)
        circuit.cx(2, 4)
    elif n == 2:
        circuit.h(0)
        circuit.cx(0, 1)

def encode(char:str, circuit: qiskit.circuit.QuantumCircuit, n: int) -> None:
    binary = get_binary(char)
    if n == 5:
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
    elif n == 2:
        if binary[5] == '1':
            circuit.z(0)
        if binary[6] == '1':
            circuit.x(0)

def delay(circuit: qiskit.circuit.QuantumCircuit, n: int) -> None:
    if n == 5:
        for i in range(16):
            circuit.i(0)
            circuit.i(1)
            circuit.i(2)
            circuit.i(3)
            circuit.i(4)
    elif n == 2:
        for i in range(16):
            circuit.i(0)
            circuit.i(1)

def decode(circuit: qiskit.circuit.QuantumCircuit, n: int) -> None:
    if n == 5:
        circuit.cx(2, 4)
        circuit.cx(1, 2)
        circuit.cx(0, 3)
        circuit.h(1)
        circuit.h(0)
    elif n == 2:
        circuit.cx(0, 1)
        circuit.h(0)

def measure(circuit: qiskit.circuit.QuantumCircuit, qr: qiskit.circuit.QuantumRegister, cr: qiskit.circuit.ClassicalRegister, n: int) -> None:
    if n == 5:
        circuit.measure(qr, cr)
    elif n == 2:
        circuit.measure(qr[0], cr[0])
        circuit.measure(qr[1], cr[1])

def reset(circuit: qiskit.circuit.QuantumCircuit, n: int):
    circuit.reset(0)
    circuit.reset(1)
    if n == 5:
        circuit.reset(2)
        circuit.reset(3)
        circuit.reset(4)

def get_char(result_counts_5: dict, result_counts_2: dict) -> str:
    result_keys_5 = list(result_counts_5)
    results_5 = [result_counts_5[i] for i in result_keys_5]
    max_val_5 = max(results_5)
    index_5 = results_5.index(max_val_5)
    key_5 = result_keys_5[index_5]
    key_5 = key_5[::-1]
    #print(key_5, max_val_5)
    
    result_keys_2 = list(result_counts_2)
    results_2 = [result_counts_2[i] for i in result_keys_2]
    max_val_2 = max(results_2)
    index_2 = results_2.index(max_val_2)
    key_2 = result_keys_2[index_2]
    key_2 = key_2[::-1]
    #print(key_2, key_2[:2], max_val_2)
    key_2 = key_2[:2]
    
    key = key_5 + key_2
    #key = key[::-1]
    #print(key)
    
    int_vers = int(key, 2)
    #print(int_vers)
    char = chr(int_vers)
    
    return char

def evaluate_error(send: str, receive: str) -> float:
    total = len(send)
    same = total
    for i in range(len(send)):
        if send[i] == receive[i]:
            same -= 1
    
    return same/total

def run(circuit: qiskit.circuit.QuantumCircuit, nshots: int, system = 'ibmq_manila', simulated = False) -> qiskit.result.Result:
    if simulated:
        qcomp = qiskit.Aer.get_backend('qasm_simulator')
    else:
        provider = qiskit.IBMQ.get_provider('ibm-q')
        qcomp = provider.get_backend(system)
    
    print('System Status: '+qcomp.status().status_msg)
    
    job = qiskit.execute(circuit, backend=qcomp, shots = nshots)
    qiskit.tools.monitor.job_monitor(job)
    
    result = job.result()
    return result

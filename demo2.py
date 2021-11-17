# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 10:17:17 2021

@author: 831995
"""

import sec_comm_7 as s7
import qiskit as q

N_LOW_ERROR = 64

def main(low_error = False, system = 'ibmq_manila', simulated = False):
    
    send_message = input('Enter Message to be Sent: ')
    receive_message = ''
    
    qlist = []
    runlist = []
    
    progress = 0
    
    for letter in send_message:
        qr5 = q.QuantumRegister(5)
        cr5 = q.ClassicalRegister(5)
        circ5 = q.QuantumCircuit(qr5, cr5)
        
        s7.initialize(circ5, 5)
        s7.encode(letter, circ5, 5)
        s7.delay(circ5, 5)
        s7.decode(circ5, 5)
        s7.measure(circ5, qr5, cr5, 5)
        
        qr2 = q.QuantumRegister(5)
        cr2 = q.ClassicalRegister(5)
        circ2 = q.QuantumCircuit(qr2, cr2)
        
        s7.initialize(circ2, 2)
        s7.encode(letter, circ2, 2)
        s7.delay(circ2, 2)
        s7.decode(circ2, 2)
        s7.measure(circ2, qr2, cr2, 2)
        
        qlist.append([circ5, circ2])
        runlist.append(circ5)
        runlist.append(circ2)
        
        progress += 1
        percent = int(100 * progress/len(send_message))
        print('\rCompile Progress: '+str(percent)+'%', end='')
        
    nshots = 1
    if low_error:
        nshots = N_LOW_ERROR
    
    print('\nBeginning Run...')
    res = s7.run(runlist, nshots, system=system, simulated=simulated)
    for circ_pair in qlist:
        result_counts_5 = res.get_counts(circ_pair[0])
        result_counts_2 = res.get_counts(circ_pair[1])
        receive_message += s7.get_char(result_counts_5, result_counts_2)
    
    print()
    print('Message Received: '+receive_message)
    print('Error Rate: '+str(int(100*s7.evaluate_error(send_message, receive_message)))+'%')

main(low_error = True, simulated = False, system = 'ibmq_bogota')
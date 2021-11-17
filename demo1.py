# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 22:08:10 2021

@author: lily
"""
import sec_comm_5 as s5
import qiskit as q

def main(low_error = False, system = 'ibmq_manila'):

    send_message = input('enter message to be sent: ')
    receive_message = ''
    
    qlist = []
    
    progress = 0
    print('progress: 0%', end='')
    
    for letter in send_message:
        qr = q.QuantumRegister(5)
        cr = q.ClassicalRegister(5)
        circ = q.QuantumCircuit(qr, cr)
        
        s5.initialize(circ)
        s5.encode(letter, circ)
        s5.delay(circ)
        s5.decode(circ)
        s5.measure(circ, qr, cr)
        
        nshots = 1
        if low_error:
            nshots = 256
        
        qlist.append(circ)
        
        progress += 1
        percent = int(100 * progress/len(send_message))
        print('\rCompile Progress: '+str(percent)+'%', end='')
    
    print('\nBeginning Run...')
    res = s5.run(qlist, nshots, system=system)
    for icirc in qlist:
        receive_message += s5.get_char(res.get_counts(icirc))

    print()
    print('message received: '+receive_message)
    print('error rate: '+str(int(100*s5.evaluate_error(send_message, receive_message)))+'%')
    
main(low_error = True, system = 'ibmq_bogota')
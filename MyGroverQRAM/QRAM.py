'''
VARIABLE MAPPER
searchedlist = search
indexs = indexes
values = values
nvalstofind = len(search) = 1
datos = values
numqbits = nr de biti necesari pentru indici + nr de biti necesari pentru valori + 1 = 5 => nbitsval + nbitsindexes
iqaux = auxq_index = 4 (al 4-lea qubit, numaratoarea incepe cu 0)
'''

from qiskit import QuantumCircuit
import matplotlib.pyplot as plt
from qiskit import Aer, execute
import operator

indexes = [0,1,2,3]
values = [1,2,0,3]
search = [2]
numqbits = 5
auxq_index = numqbits-1

qc = QuantumCircuit(numqbits, numqbits)

nbitsval = int(len(values)/2)
nbitsindexes = int(len(indexes)/2)
'''
A problem with this approach is that we can't put values in the database that have a binary representation that needs more bits than the number of indexes available...
For example, if we have only two qubits for our indexes (so indexes 0,1,2 and 3), that means we can only have the values [0,1,2,3] in our database, but it doesn't have to be all:
For example, we could have 2 index qubits and the values [0,3,1,0] 
'''
nregsdb = len(indexes)

# HELPER FUNCTIONS
def binary_format(x, n=0):    
    return format(x, 'b').zfill(n)
def reversed_string(a_string):
    return a_string[::-1]

def indexMCX(controls,nbitsindexes,targetbit,reversed_binary_index):  
    '''
    Function that uses the index values as control qubits for flipping each bit of the value
    For example, for index 0 and value 3, we'll need to flip both qubits of index "00" to "11" so they can be used to flip the first and second qubits of 
    reversed binary value "11" for "3"
    This basically solves the issue of "gaps" in the database, as the indexes will always be continuous and the values will have "0" as a coventional "NULL" value.
    '''      
    for i in range(nbitsindexes):
        if reversed_binary_index[i] == '0': # if the index bit is 0, make it a 1, so we can use it to activate the target qubit          
            qc.x(controls[i])
        # If it's already 1, then we can already use it
    # Use the index qubits as controls for activating the target qubit
    qc.mcx(controls,targetbit)
    
    for i in range(nbitsindexes-1,-1,-1): # If the qubits were 0, and we activated them in order to activate the value, we need to put it back
        if reversed_binary_index[i] == '0':
            qc.x(controls[i])   

qc.h(range(nbitsindexes))
qc.x(auxq_index)

# DB INIT
controls = []
for i in range(nbitsindexes):
    controls.append(i)
for i in range(nregsdb):
    reversed_binary_index= reversed_string(binary_format(indexes[i],nbitsindexes))
    print(f"Reversed binary representation for index: {reversed_binary_index}")
    reversed_binary_value = reversed_string(binary_format(values[i],nbitsval))
    print(f"Reversed binary representation for value: {reversed_binary_value}")
    for j in range(nbitsval):
        if reversed_binary_value[j] == '1':
            targetbit = j + nbitsindexes
            print(f"Applying ctrlarrayx for bit {j} of reversed binary value {reversed_binary_value}, which means for qubit {targetbit}")
            indexMCX(controls,nbitsindexes,targetbit,reversed_binary_index)

# ORACLE DESIGN

controls = []
for i in range(nbitsval):
    controls.append(nbitsindexes + i)
searched_value = binary_format(search[0], nbitsval) # Keep in mind that we're looking only for one value
# "Activate" qubits in value register - Which means putting the correct qubits into superposition now!
# This is the variant of the grover algorithm that uses an auxiliary qubit
for i in range(nbitsval):
    if searched_value[(nbitsval - 1) - i] == '0':
        qc.x(nbitsindexes+i)
qc.h(auxq_index)
qc.mcx(controls, auxq_index)
qc.h(auxq_index)
for i in range(nbitsval):
    if searched_value[(nbitsval - 1) - i] == '0':
        qc.x(nbitsindexes+i)

# DB INIT
controls = []
for i in range(nbitsindexes):
    controls.append(i)
for i in range(nregsdb):
    reversed_binary_index= reversed_string(binary_format(indexes[i],nbitsindexes))
    print(f"Reversed binary representation for index: {reversed_binary_index}")
    reversed_binary_value = reversed_string(binary_format(values[i],nbitsval))
    print(f"Reversed binary representation for value: {reversed_binary_value}")
    for j in range(nbitsval):
        if reversed_binary_value[j] == '1':
            targetbit = j + nbitsindexes
            print(f"Applying ctrlarrayx for bit {j} of reversed binary value {reversed_binary_value}, which means for qubit {targetbit}")
            indexMCX(controls,nbitsindexes,targetbit,reversed_binary_index)

# AMPLIFY STEP
controls = []
for i in range(nbitsindexes):
    controls.append(i)
qc.h(range(nbitsindexes))
qc.x(range(nbitsindexes))
qc.h(auxq_index)    
qc.mcx(controls,auxq_index)
qc.h(auxq_index)        
qc.x(range(nbitsindexes))
qc.h(range(nbitsindexes))    
qc.measure(range(nbitsindexes), range(nbitsindexes))



# SIMULATE STEP
results = []
backend = Aer.get_backend('aer_simulator')        
job = execute(qc, backend, shots = 100)
# Grab the results from the job.
result = job.result()
counts = result.get_counts(qc)
print(counts)
qc.draw(output='mpl')
plt.show()





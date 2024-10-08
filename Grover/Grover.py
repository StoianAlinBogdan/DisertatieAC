import matplotlib.pyplot as plt
from qiskit import *
from qiskit.circuit.library import Diagonal
from qiskit.quantum_info import Statevector, DensityMatrix, Operator

# Generate the oracle for the searched state

mark_state = Statevector.from_label("01011")
mark_circuit = Diagonal((-1)**mark_state.data)
qc = QuantumCircuit(5)
for i in range(5):
    qc.h(i)

qc.append(mark_circuit, [0, 1, 2, 3, 4])
for i in range(5):
    qc.h(i)

diffuse_operator = 2 * DensityMatrix.from_label(5 * '0') - Operator.from_label(5 * 'I')
diffuse_circuit = Diagonal(diffuse_operator.data.diagonal())
qc.append(diffuse_circuit, [0, 1, 2, 3, 4])
for i in range(5):
    qc.h(i)

qc.append(mark_circuit, [0, 1, 2, 3, 4])
for i in range(5):
    qc.h(i)
qc.append(diffuse_circuit, [0, 1, 2, 3, 4])
for i in range(5):
    qc.h(i)
qc.append(mark_circuit, [0, 1, 2, 3, 4])
for i in range(5):
    qc.h(i)
qc.append(diffuse_circuit, [0, 1, 2, 3, 4])
for i in range(5):
    qc.h(i)

qc.measure_all()
simulator = Aer.get_backend('qasm_simulator')
result = execute(qc, backend = simulator, shots = 2048).result()
counts = result.get_counts()
print('RESULT: ',counts,'\n')


qc.draw(output='mpl')
plt.show()

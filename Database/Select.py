from qiskit import QuantumCircuit, Aer, execute, Statevector
from qiskit.quantum_info.operators import Operator
from math import sqrt
import numpy as np
from qiskit_algorithms import Grover
from qiskit.primitives import Sampler

def is_unitary(matrix: np.ndarray) -> bool:

    unitary = True
    n = len(matrix)
    error = np.linalg.norm(np.eye(n) - matrix.dot( matrix.transpose().conjugate()))

    if not(error < np.finfo(matrix.dtype).eps * 10.0 *n):
        unitary = False
    return unitary


qc = QuantumCircuit(4)
qc.h(0)
qc.h(1)
qc.h(2)

qc.cnot(0, 3)
qc.cnot(1, 3)
qc.cnot(2, 3)

oracle = Statevector.from_label('1111')

qc.measure_all()
print(qc)

sim = Aer.get_backend('statevector_simulator')
res = execute(qc, sim, shots=1000).result()
counts = res.get_counts()
print(counts)
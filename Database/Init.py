from qiskit.quantum_info.operators import Operator
from qiskit import QuantumCircuit, Aer, execute
from qiskit.quantum_info import Statevector
from qiskit_algorithms import AmplificationProblem
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram

qc = QuantumCircuit(3)
qc.h(0)
qc.h(1)
# We insert the first and second qubits in equal superposition
# Therefore, the database contains the values 000, 010, 100 and 110
# (Qubits are bigendian!)

cx = Operator([
    [1, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 0]
])

qc.unitary(cx, [0,1,2], label='cx') # database now contains 000, 010, 100, and 111 (state 011 was changed to 111) 

mark = Statevector.from_label('100')
problem = AmplificationProblem(mark, is_good_state=['100'])
qc = qc.compose(problem.grover_operator)
#qc = qc.compose(problem.grover_operator)

qc.measure_all()
qc.draw(output='mpl')
plt.show()

sim = Aer.get_backend('statevector_simulator')
res = execute(qc, sim, shots=10000).result()
counts = res.get_counts()
print(counts)
plot_histogram(counts, legend=["Count of\n results out\n of 10000\n executions"], sort="value")
plt.show()




import numpy as np
from numpy.random import choice

class gates:
    single_q = {'x':np.array([[0, 1], [1, 0]]),
                      'h':np.array([[1/np.sqrt(2), 1/np.sqrt(2)], [1/np.sqrt(2), -1/np.sqrt(2)]])}
    multi_q = {'cx':np.array([[0, 1], [1, 0]])}

class matrices:
    I = np.identity(2)
    P0X0 = np.array([[1, 0],[0, 0]])
    P1X1 = np.array([[0, 0],[0, 1]])

class quantum_circuit:
    def __init__(self, num_qubits, circuit=[]):
        self.num_qubits = num_qubits
        self.state = np.zeros_like(np.arange(2**num_qubits))
        self.state[0]=1
        self.circuit = circuit

    def x(self, target):
        x = { "gate": "x", "target": [target] }
        self.circuit.append(x)

    def h(self, target):
        h = { "gate": "h", "target": [target] }
        self.circuit.append(h)

    def cx(self, control, target):
        cx = { "gate": "cx", "target": [control, target] }
        self.circuit.append(cx)

    def get_operator(self, gate_unitary, target_qubits):
        if gate_unitary in gates.single_q:
            target = target_qubits[0]
            operator = 1
            for i in range(self.num_qubits):
                if i == target_qubits[0]:
                    operator = np.kron(operator, gates.single_q[gate_unitary])
                else:
                    operator = np.kron(operator, matrices.I)
            return operator
        elif gate_unitary in gates.multi_q:
            control = target_qubits[0]
            target = target_qubits[1]
            operator_a = 1
            operator_b = 1
            for i in range(self.num_qubits):
                if i == control:
                    operator_a = np.kron(operator_a, matrices.P0X0)
                    operator_b = np.kron(operator_b, matrices.P1X1)
                elif i == target:
                    operator_a = np.kron(operator_a, matrices.I)
                    operator_b = np.kron(operator_b, gates.multi_q[gate_unitary])
                else:
                    operator_a = np.kron(operator_a, matrices.I)
                    operator_b = np.kron(operator_b, matrices.I)
            return operator_a + operator_b
    
    def run(self):
        for operation in self.circuit:
            gate, target = operation['gate'], operation['target']
            operator = self.get_operator(gate, target)
            self.state = np.dot(operator, self.state)

    def measure_all(self):
        return "{0:b}".format(choice(range(len(self.state)), 1, p=np.square(self.state))[0]).zfill(self.num_qubits)
    
    def get_counts(self, num_shots):
        counts = {}
        for i in range(num_shots):
            measurement = self.measure_all()
            if measurement not in counts.keys():
                counts[measurement] = 1
            else:
                counts[measurement] += 1 
        return counts

c = my_circuit = [
{ "gate": "x", "target": [0] },
{ 'gate': 'cx', 'target': [0,2] },
{ 'gate': 'h', 'target':[2]}
]

qc = quantum_circuit(4)
qc.x(0)
qc.cx(0,2)
qc.h(2)
qc.run()
counts = qc.get_counts(1000)
print(counts)
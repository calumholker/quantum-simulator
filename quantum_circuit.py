import numpy as np
from numpy.random import choice

class gates:
    single_q = {
                'x': np.array([[0, 1], [1, 0]]),
                'y': np.zeros((2, 2), dtype=np.complex_) + [[0, complex(0, -1)], [complex(0, 1), 0]],
                'z': np.array([[1, 0], [0, -1]]),
                'h': np.array([[1/np.sqrt(2), 1/np.sqrt(2)], [1/np.sqrt(2), -1/np.sqrt(2)]]),
                }
    multi_q = {
                'cx': np.array([[0, 1], [1, 0]]),
                'cy': np.zeros((2, 2), dtype=np.complex_) + [[0, complex(0, -1)], [complex(0, 1), 0]],
                'cz': np.array([[1, 0], [0, -1]])
                }
    parameter_q = ['u3']

class matrices:
    I = np.identity(2)
    P0X0 = np.array([[1, 0],[0, 0]])
    P1X1 = np.array([[0, 0],[0, 1]])

class quantum_circuit:
    def __init__(self, num_qubits, circuit=[]):
        self.num_qubits = num_qubits
        self.state = np.zeros_like(np.arange(2**num_qubits))
        self.state[0]=1
        self.params = []
        self.circuit = circuit

    def x(self, target):
        x = { "gate": "x", "target": [target] }
        self.circuit.append(x)

    def y(self, target):
        y = { "gate": "y", "target": [target] }
        self.circuit.append(y)

    def z(self, target):
        z = { "gate": "z", "target": [target] }
        self.circuit.append(z)

    def h(self, target):
        h = { "gate": "h", "target": [target] }
        self.circuit.append(h)

    def cx(self, control, target):
        cx = { "gate": "cx", "target": [control, target] }
        self.circuit.append(cx)

    def cy(self, control, target):
        cy = { "gate": "cy", "target": [control, target] }
        self.circuit.append(cy)

    def cz(self, control, target):
        cz = { "gate": "cz", "target": [control, target] }
        self.circuit.append(cz)

    def u3(self, target, params):
        u3 = { "gate": "u3", "target": [target], "params" : params}
        self.circuit.append(u3)

    def get_operator(self, gate_unitary, target_qubits, parameters = None):
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
        elif gate_unitary in gates.parameter_q:
            target = target_qubits[0]
            phi = parameters['phi']
            theta = parameters['theta']
            lamb = parameters['lambda']
            if phi in self.params:
                phi = self.params[phi]
            if theta in self.params:
                theta = self.params[theta]
            if lamb in self.params:
                lamb = self.params[lamb]
            param_gate = np.array([[np.cos(theta/2) , -np.e**(complex(0,1)*lamb)*np.sin(theta/2)],
                                   [np.e**(complex(0,1)*phi)*np.sin(theta/2) , np.e**(complex(0,1)*(phi+lamb))*np.cos(theta/2)]])
            operator = 1
            for i in range(self.num_qubits):
                if i == target_qubits[0]:
                    operator = np.kron(operator, param_gate)
                else:
                    operator = np.kron(operator, matrices.I)
            return operator
    
    def run(self, params = None, initial_state = None):
        if initial_state != None:
            self.state = np.array(initial_state)
        if params != None:
            self.params = params
        for operation in self.circuit:
            gate, target = operation['gate'], operation['target']
            params = operation.get('params')
            operator = self.get_operator(gate, target, params)
            self.state = np.dot(operator, self.state)

    def measure_all(self):
        return "{0:b}".format(choice(range(len(self.state)), 1, p=np.square(abs(self.state)))[0]).zfill(self.num_qubits)
    
    def get_counts(self, num_shots):
        counts = {}
        for i in range(num_shots):
            measurement = self.measure_all()
            if measurement not in counts.keys():
                counts[measurement] = 1
            else:
                counts[measurement] += 1 
        return counts
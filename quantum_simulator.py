import numpy as np
from numpy.random import choice

class gates:
    q_gates = {
                'x': np.array([[0, 1], [1, 0]]),
                'y': np.zeros((2, 2), dtype=np.complex_) + [[0, complex(0, -1)], [complex(0, 1), 0]],
                'z': np.array([[1, 0], [0, -1]]),
                'h': np.array([[1/np.sqrt(2), 1/np.sqrt(2)], [1/np.sqrt(2), -1/np.sqrt(2)]]),
                'cx': np.array([[0, 1], [1, 0]]),
                'cy': np.zeros((2, 2), dtype=np.complex_) + [[0, complex(0, -1)], [complex(0, 1), 0]],
                'cz': np.array([[1, 0], [0, -1]])
                }

class matrices:
    I = np.identity(2)
    P0X0 = np.array([[1, 0],[0, 0]])
    P1X1 = np.array([[0, 0],[0, 1]])
    PqXq = [P0X0, P1X1]

class quantum_circuit:
    def __init__(self, num_qubits, circuit=[]):
        self.num_qubits = num_qubits
        self.state = np.zeros_like(np.arange(2**num_qubits))
        self.state[0]=1
        self.params = []
        self.circuit = circuit

    def get_operator(self, gate, target_qubits, parameters = None):
        controls = target_qubits[0]
        targets = target_qubits[1]
        cases = []
        if gate in gates.q_gates:
            matrix = gates.q_gates[gate]
        elif gate == 'u3':
            phi = parameters['phi']
            theta = parameters['theta']
            lamb = parameters['lambda']
            if phi in self.params:
                phi = self.params[phi]
            if theta in self.params:
                theta = self.params[theta]
            if lamb in self.params:
                lamb = self.params[lamb]
            matrix = np.array([[np.cos(theta/2) , -np.e**(complex(0,1)*lamb)*np.sin(theta/2)],
                                [np.e**(complex(0,1)*phi)*np.sin(theta/2) , np.e**(complex(0,1)*(phi+lamb))*np.cos(theta/2)]])
        else:
            return 1
        for i in range(2**len(controls)):
            cases.append(1)
        for i in range(len(cases)):
            bin_i = [int(x) for x in bin(i)[2:].zfill(len(controls))]
            count_controls = 0
            for j in range(self.num_qubits):
                if j in controls:
                    cases[i] = np.kron(cases[i], matrices.PqXq[bin_i[count_controls]])
                    count_controls += 1
                elif j in targets:
                    if i != (len(cases)-1):
                        cases[i] = np.kron(cases[i], matrices.I)
                    else:
                            cases[i] = np.kron(cases[i], matrix)
                else:
                    cases[i] = np.kron(cases[i], matrices.I)
        return sum(cases)
    
    def run(self, params = None, initial_state = None):
        if initial_state != None:
            self.state = np.array(initial_state)
        if params != None:
            self.params = params
        for operation in self.circuit:
            gate, controls, targets = operation['gate'], operation['controls'], operation['targets']
            parameters = operation.get('params')
            operator = self.get_operator(gate, [controls, targets], parameters)
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
    
    def x(self, targets):
        x = { "gate": "x", "controls": [], "targets": targets }
        self.circuit.append(x)

    def y(self, targets):
        y = { "gate": "y", "controls": [], "targets": targets }
        self.circuit.append(y)

    def z(self, targets):
        z = { "gate": "z", "controls": [], "targets": targets }
        self.circuit.append(z)

    def h(self, targets):
        h = { "gate": "h", "controls": [], "targets": targets }
        self.circuit.append(h)

    def mx(self, controls, targets):
        cx = { "gate": "cx", "controls": controls, "targets": targets }
        self.circuit.append(cx)

    def my(self, controls, targets):
        cy = { "gate": "cy", "controls": controls, "targets": targets }
        self.circuit.append(cy)

    def mz(self, controls, targets):
        cz = { "gate": "cz", "controls": controls, "targets": targets }
        self.circuit.append(cz)

    def u3(self, targets, params):
        u3 = { "gate": "u3", "controls": [], "targets": targets, "params" : params}
        self.circuit.append(u3)

    def mu3(self, controls, targets, params):
        multi = { "matrix": "u3" ,"controls": controls, "targets": targets, "params": params}
        self.circuit.append(multi)
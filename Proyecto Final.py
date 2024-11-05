from collections import deque

class TuringMachine:
    def __init__(self, states, symbols, tape_alphabet, transitions, initial_state, blank_symbol, final_states):
        self.states = states
        self.symbols = symbols
        self.tape_alphabet = tape_alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.blank_symbol = blank_symbol
        self.final_states = final_states
        self.tape1 = []
        self.tape2 = []
        self.head1 = 0
        self.head2 = 0
        self.current_state = initial_state

    def load_input(self, input_string):
        # Load the input into tape1 and initialize tape2 with blanks
        self.tape1 = list(input_string) + [self.blank_symbol]
        self.tape2 = [self.blank_symbol] * len(self.tape1)
        self.head1 = 0
        self.head2 = 0
        self.current_state = self.initial_state

    def step(self):
        # Ensure heads are within bounds
        if self.head1 < 0:
            self.head1 = 0
            self.tape1.insert(0, self.blank_symbol)
        elif self.head1 >= len(self.tape1):
            self.tape1.append(self.blank_symbol)

        if self.head2 < 0:
            self.head2 = 0
            self.tape2.insert(0, self.blank_symbol)
        elif self.head2 >= len(self.tape2):
            self.tape2.append(self.blank_symbol)

        # Perform one step based on the current state and symbols on both tapes
        if (self.current_state, self.tape1[self.head1], self.tape2[self.head2]) in self.transitions:
            new_state, write_symbol1, write_symbol2, move1, move2 = self.transitions[
                (self.current_state, self.tape1[self.head1], self.tape2[self.head2])]
            self.tape1[self.head1] = write_symbol1
            self.tape2[self.head2] = write_symbol2
            self.current_state = new_state

            # Move the heads
            if move1 == 'R':
                self.head1 += 1
            elif move1 == 'L':
                self.head1 -= 1
            if move2 == 'R':
                self.head2 += 1
            elif move2 == 'L':
                self.head2 -= 1
        else:
            return False  # No valid transition found
        return True

    def run(self):
        # Run the Turing machine until it reaches a final state or no more transitions are possible
        while self.current_state not in self.final_states:
            if not self.step():
                break
        return self.current_state in self.final_states

    def print_transition_table(self):
        # Print the transition table for debugging or demonstration purposes
        print("\nTabla de Transición:")
        print("Estado Actual | Símbolo Cinta1 | Símbolo Cinta2 | Nuevo Estado | Símbolo Cinta1 | Símbolo Cinta2 | Movimiento Cinta1 | Movimiento Cinta2")
        for (state, symbol1, symbol2), (new_state, write1, write2, move1, move2) in self.transitions.items():
            print(f"{state:<13} | {symbol1:<13} | {symbol2:<13} | {new_state:<11} | {write1:<13} | {write2:<13} | {move1:<16} | {move2}")

    def generate_derivation_tree(self, input_string):
        print(f"\nÁrbol de derivación de la cadena '{input_string}':")
        def _print_tree(indent, symbol):
            print(" " * indent + f"|- {symbol}")
            return indent + 2
        indent = _print_tree(0, "S")
        for char in input_string:
            indent = _print_tree(indent, char)

    def display_tapes(self):
        # Show the content of both tapes in both directions
        tape1_content = ''.join(self.tape1).strip()
        tape2_content = ''.join(self.tape2).strip()
        print(f"\nCinta 1 (Izquierda a Derecha): {tape1_content}")
        print(f"Cinta 1 (Derecha a Izquierda): {tape1_content[::-1]}")
        print(f"Cinta 2 (Izquierda a Derecha): {tape2_content}")
        print(f"Cinta 2 (Derecha a Izquierda): {tape2_content[::-1]}")

# Configuración de la máquina de Turing
states = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'qf'}
symbols = {'a', 'b', '#', '*'}
tape_alphabet = {'a', 'b', '#', '*', ' '}
initial_state = 'q0'
blank_symbol = ' '
final_states = {'qf'}

transitions = {
    # Transiciones iniciales para procesar los primeros caracteres en ambas cintas
    ('q0', 'a', ' '): ('q1', 'a', 'a', 'R', 'R'),
    ('q0', 'a', 'a'): ('q1', 'a', 'a', 'R', 'R'),
    
    # Transiciones para secuencia 'b' después de 'a' en ambas cintas
    ('q1', 'b', ' '): ('q2', 'b', 'b', 'R', 'R'),
    ('q1', 'b', 'b'): ('q2', 'b', 'b', 'R', 'R'),
    
    # Transiciones para otra 'a' después de 'b' en ambas cintas
    ('q2', 'a', ' '): ('q3', 'a', 'a', 'R', 'R'),
    ('q2', 'a', 'a'): ('q3', 'a', 'a', 'R', 'R'),
    
    # Segunda 'a' en la secuencia
    ('q3', 'a', ' '): ('q4', 'a', 'a', 'R', 'R'),
    ('q3', 'a', 'a'): ('q4', 'a', 'a', 'R', 'R'),
    
    # Transición para 'b' después de 'a a'
    ('q4', 'b', ' '): ('q5', 'b', 'b', 'R', 'R'),
    ('q4', 'b', 'b'): ('q5', 'b', 'b', 'R', 'R'),
    
    # Transición para '*'
    ('q5', '*', ' '): ('q6', '*', '*', 'R', 'R'),
    ('q5', '*', '*'): ('q6', '*', '*', 'R', 'R'),
    
    # Transición para '#' después de '*'
    ('q6', '#', ' '): ('q7', '#', '#', 'R', 'R'),
    ('q6', '#', '#'): ('q7', '#', '#', 'R', 'R'),
    
    # Transiciones de repetición para 'a' y 'b' en ambas cintas después de '#'
    ('q7', 'a', ' '): ('q7', 'a', 'a', 'R', 'R'),
    ('q7', 'a', 'a'): ('q7', 'a', 'a', 'R', 'R'),
    ('q7', 'b', ' '): ('q7', 'b', 'b', 'R', 'R'),
    ('q7', 'b', 'b'): ('q7', 'b', 'b', 'R', 'R'),
    
    # Estado final
    ('q7', ' ', ' '): ('qf', ' ', ' ', 'R', 'R')
}

tm = TuringMachine(states, symbols, tape_alphabet, transitions, initial_state, blank_symbol, final_states)

# Leer cadenas de un archivo y procesarlas
def procesar_cadenas(archivo_cadenas):
    with open(archivo_cadenas, 'r') as archivo:
        cadenas = archivo.read().splitlines()
    
    # Procesar cada cadena
    cadenas_validas = []
    cadenas_invalidas = []
    
    for cadena in cadenas:
        print("\n" + "="*50)
        print(f"\nProcesando cadena: '{cadena}'")
        
        # Cargar la cadena en la máquina
        tm.load_input(cadena)
        
        # Imprimir tabla de transición específica
        tm.print_transition_table()
        
        # Ejecutar la máquina de Turing
        resultado = tm.run()
        print(f"\nCadena: '{cadena}' - {'Válida' if resultado else 'Inválida'}")
        
        if resultado:
            cadenas_validas.append(cadena)
        else:
            cadenas_invalidas.append(cadena)
        
        # Generar el árbol de derivación
        tm.generate_derivation_tree(cadena)
        
        # Mostrar el contenido de ambas cintas
        tm.display_tapes()
        
        # Simulación de la pila (representada como lista para los propósitos del árbol de derivación)
        pila = deque()
        print(f"\nSimulación de pila para '{cadena}':")
        for char in cadena:
            pila.append(char)
            print(f"Apilar: {char} - Pila: {list(pila)}")
        while pila:
            char = pila.pop()
            print(f"Desapilar: {char} - Pila: {list(pila)}")
    
    # Resumen final
    print("\nResumen Final:")
    print(f"\nCadenas válidas ({len(cadenas_validas)}):")
    for s in cadenas_validas:
        print(s)
    print(f"\nCadenas inválidas ({len(cadenas_invalidas)}):")
    for s in cadenas_invalidas:
        print(s)

# Ejecutar el procesamiento
procesar_cadenas(r'C:\Users\upa21\OneDrive\Escritorio\Python\cadenas.txt')

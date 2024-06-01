import random

def generate_random_fsm(num_states, num_outputs, num_inputs, initial_connected, partialness):
    fsm = {state: {} for state in range(num_states)}
    for state in range(num_states):
        for inp in range(num_inputs):
            if random.random() < partialness:  # Check if transition should be defined
                next_state = random.randint(0, num_states - 1)
                output = random.randint(0, num_outputs - 1)
                fsm[state][inp] = (next_state, output)

    if initial_connected:
        # Ensure the FSM is initially connected
        visited = set()
        stack = [0]  # Start from the initial state
        while stack:
            current_state = stack.pop()
            if current_state not in visited:
                visited.add(current_state)
                for next_state, _ in fsm[current_state].values():
                    if next_state not in visited:
                        stack.append(next_state)
        
        # Check if all states are reachable
        if len(visited) < num_states:
            return False, None
    
    return True, fsm

num_fsms = int(input("Enter the number of FSMs to be generated: "))
num_states = int(input("Enter the number of states: "))
num_inputs = int(input("Enter the number of inputs: "))
num_outputs = int(input("Enter the number of outputs: "))
initial_connected_percentage = float(input("Enter the percentage of FSMs that should be initially connected (0 to 1): "))
partialness_percentage = float(input("Enter the percentage of FSMs that should be partial (0 to 1): "))

output_file = './generated_fsms.txt'
num_initially_connected = 0
num_complete_fsms = 0

with open(output_file, 'w') as f:
    fsm_id = 0
    for fsm_num in range(num_fsms):
        initial_connected = random.random() < initial_connected_percentage
        partialness = partialness_percentage if random.random() < partialness_percentage else 1.0
        while True:
            success, random_fsm = generate_random_fsm(num_states, num_outputs, num_inputs, initial_connected, partialness)
            if success:
                if initial_connected:
                    num_initially_connected += 1
                # Check if the FSM is complete
                is_complete = all(len(transitions) == num_inputs for transitions in random_fsm.values())
                if is_complete:
                    num_complete_fsms += 1
                break
        
        total_transitions = sum(len(transitions) for transitions in random_fsm.values())
        f.write(f"{fsm_id} {num_states} {total_transitions} {num_inputs} {num_outputs} void-data\n")
        fsm_id += 1
        for state, transitions in random_fsm.items():
            for inp, (next_state, output) in transitions.items():
                f.write(f"{state} {next_state} {chr(97 + inp)} {output}\n")

print(f"Number of initially connected FSMs: {num_initially_connected}")
print(f"Number of complete FSMs: {num_complete_fsms}")

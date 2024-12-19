import tkinter as tk
from tkinter import messagebox
# from graphviz import Digraph
import graphviz
from PIL import Image,ImageTk
import os

def generate_fsm_diagram(states, transitions, start_state, accept_states):
    try:
        dot = graphviz.Digraph()

        # Add nodes for all states
        for state in states:
            if state in accept_states:
                dot.node(state, shape='doublecircle')  # Accept states have double circles
            else:
                dot.node(state)

        # Add an invisible start node pointing to the start state
        dot.node('start', shape='none')
        dot.edge('start', start_state)

        # Add edges for transitions
        for transition in transitions:
            src, sym, dest = transition.split(',')
            dot.edge(src, dest, label=sym)

        # Render the diagram
        dot.render('pic', format='jpg', cleanup=True)
    except Exception as e:
        print(e)
        messagebox.showerror("Error", f"Could not generate FSM diagram: {e}")

def simulate_dfsm():
    try:
        # Parse input
        states = state_entry.get().split(',')
        alphabet = alphabet_entry.get().split(',')
        start_state = start_state_entry.get()
        accept_states = accept_state_entry.get().split(',')
        transitions = transition_entry.get().split(';')  # Fix: Split by semicolon
        input_string = input_string_entry.get()

        # Create a transition dictionary
        transition_dict = {}
        for trans in transitions:
            # Ensure the transition format is correct
            if trans.count(',') == 2:  # This checks that the transition format is 'state,symbol,next_state'
                src, sym, dest = trans.split(',')
                if (src, sym) not in transition_dict:
                    transition_dict[(src, sym)] = dest
            else:
                messagebox.showerror("Error", "Invalid transition format. Each transition should be 'state,symbol,next_state'.")
                return

        # Generate FSM diagram
        generate_fsm_diagram(states, transitions, start_state, accept_states)

        # Display FSM diagram in the GUI
        if os.path.exists('pic.jpg'):
            img = ImageTk.PhotoImage(Image.open('pic.jpg'))
            fsm_diagram_label.config(image=img)
            fsm_diagram_label.image = img

        # Simulate the DFSM
        current_state = start_state
        for char in input_string:
            if (current_state, char) in transition_dict:
                current_state = transition_dict[(current_state, char)]
            else:
                result_label.config(text="Result: String Rejected", fg="red")
                return

        # Check if the final state is accepting
        if current_state in accept_states:
            result_label.config(text="Result: String Accepted", fg="green")
        else:
            result_label.config(text="Result: String Rejected", fg="red")
    except Exception as e:
        messagebox.showerror("Error", f"Simulation failed: {e}")

# GUI Setup
root = tk.Tk()
root.title("Simulation of Deterministic Finite State Machines (DFSM) Using Python")
root.geometry("1200x600")

# Frames for Input and Output
input_frame = tk.Frame(root, padx=10, pady=10, bg="#02c2e8", relief="groove", bd=2)
input_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

output_frame = tk.Frame(root, padx=10, pady=10, bg="lightgrey", relief="groove", bd=2)
output_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

# Input Fields
input_title = tk.Label(input_frame, text="Input Section", font=("Arial", 14, "bold"), bg="#02c2e8")
input_title.grid(row=0, column=0, columnspan=2, pady=10)

state_label = tk.Label(input_frame, text="Enter States (comma-separated):", bg="#02c2e8")
state_label.grid(row=1, column=0, sticky="w", pady=5)
state_entry = tk.Entry(input_frame, width=30)
state_entry.grid(row=1, column=1, pady=5)

alphabet_label = tk.Label(input_frame, text="Enter Alphabet (comma-separated):", bg="#02c2e8")
alphabet_label.grid(row=2, column=0, sticky="w", pady=5)
alphabet_entry = tk.Entry(input_frame, width=30)
alphabet_entry.grid(row=2, column=1, pady=5)

start_state_label = tk.Label(input_frame, text="Enter Start State:", bg="#02c2e8")
start_state_label.grid(row=3, column=0, sticky="w", pady=5)
start_state_entry = tk.Entry(input_frame, width=30)
start_state_entry.grid(row=3, column=1, pady=5)

accept_state_label = tk.Label(input_frame, text="Enter Accepting States (comma-separated):", bg="#02c2e8")
accept_state_label.grid(row=4, column=0, sticky="w", pady=5)
accept_state_entry = tk.Entry(input_frame, width=30)
accept_state_entry.grid(row=4, column=1, pady=5)

transition_label = tk.Label(input_frame, text="Enter Transitions (state,symbol,next_state;...):", bg="#02c2e8")
transition_label.grid(row=5, column=0, sticky="w", pady=5)
transition_entry = tk.Entry(input_frame, width=30)
transition_entry.grid(row=5, column=1, pady=5)

input_string_label = tk.Label(input_frame, text="Enter String to Verify:", bg="#02c2e8")
input_string_label.grid(row=6, column=0, sticky="w", pady=5)
input_string_entry = tk.Entry(input_frame, width=30)
input_string_entry.grid(row=6, column=1, pady=5)

simulate_button = tk.Button(input_frame, text="Simulate DFSM", command=simulate_dfsm, bg="white", fg="black")
simulate_button.grid(row=7, column=0, columnspan=2, pady=10)

# Output Section
output_title = tk.Label(output_frame, text="Output Section", font=("Arial", 14, "bold"), bg="lightgrey")
output_title.grid(row=0, column=0, pady=10)

fsm_diagram_label = tk.Label(output_frame, bg="lightgrey")
fsm_diagram_label.grid(row=1, column=0, pady=10)

result_label = tk.Label(output_frame, text="Result:", font=("Arial", 12), bg="lightgrey")
result_label.grid(row=2, column=0, pady=10)

root.mainloop()
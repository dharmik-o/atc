import tkinter as tk
from tkinter import messagebox
import graphviz
from PIL import Image, ImageTk
import os

def generate_nfa_diagram(states, transitions, start_state, accept_states):
    try:
        dot = graphviz.Digraph()
        for state in states:
            if state in accept_states:
                dot.node(state, shape='doublecircle')
            else:
                dot.node(state)

        dot.node('start', shape='none')
        dot.edge('start', start_state)
        for transition in transitions:
            src, sym, dest = transition.split(',')
            dest_states = dest.split('|')  
            for dst in dest_states:
                dot.edge(src, dst, label=sym)

        dot.render('nfa_diagram', format='jpg', cleanup=True)
    except Exception as e:
        messagebox.showerror("Error", f"Could not generate NFA diagram: {e}")

def extract_required_transitions(transitions):
    """Extract transitions required for the NFA."""
    nfa_transitions = {}
    for trans in transitions:
        src, sym, dest = trans.split(',')
        if (src, sym) not in nfa_transitions:
            nfa_transitions[(src, sym)] = set()
        nfa_transitions[(src, sym)].add(dest)
    nfa_formatted_transitions = []
    for (src, sym), dest_set in nfa_transitions.items():
        dest = '|'.join(dest_set) 
        nfa_formatted_transitions.append(f"{src},{sym},{dest}")
    return nfa_formatted_transitions

def simulate_nfa():
    try:
        states = state_entry.get().split(',')
        start_state = start_state_entry.get()
        accept_states = set(accept_state_entry.get().split(','))
        nfa_transitions = extract_required_transitions(transition_entry.get().split(' '))
        input_string = input_string_entry.get()       
        transition_dict = {}
        for trans in nfa_transitions:
            src, sym, dest = trans.split(',')
            if (src, sym) not in transition_dict:
                transition_dict[(src, sym)] = set()
            transition_dict[(src, sym)].update(dest.split('|'))
        current_states = {start_state} 
        for char in input_string:
            next_states = set()
            for state in current_states:
                if (state, char) in transition_dict:
                    next_states.update(transition_dict[(state, char)])
            current_states = next_states
            if not current_states: 
                result_label.config(text="Result: String Rejected", fg="red")
                return
        if current_states & accept_states:
            result_label.config(text="Result: String Accepted", fg="green")
        else:
            result_label.config(text="Result: String Rejected", fg="red")
    except Exception as e:
        messagebox.showerror("Error", f"Simulation failed: {e}")
        
def dfa_to_nfa():
    try:
        states = state_entry.get().split(',')
        start_state = start_state_entry.get()
        accept_states = accept_state_entry.get().split(',')
        dfa_transitions = transition_entry.get().split(' ')
        nfa_transitions = extract_required_transitions(dfa_transitions)
        generate_nfa_diagram(states, nfa_transitions, start_state, accept_states)
        if os.path.exists('nfa_diagram.jpg'):
            img = ImageTk.PhotoImage(Image.open('nfa_diagram.jpg'))
            nfa_diagram_label.config(image=img)
            nfa_diagram_label.image = img
        result_label.config(text="NFA generated successfully.", fg="green")
    except Exception as e:
        messagebox.showerror("Error", f"Conversion failed: {e}")

root = tk.Tk()
root.title("DFA to NFA Converter and String Tester")
root.geometry("1200x600")

input_frame = tk.Frame(root, padx=10, pady=10, bg="lightblue", relief="groove", bd=2)
input_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

output_frame = tk.Frame(root, padx=10, pady=10, bg="lightgrey", relief="groove", bd=2)
output_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)
input_title = tk.Label(input_frame, text="Input Section", font=("Arial", 14, "bold"), bg="lightblue")
input_title.grid(row=0, column=0, columnspan=2, pady=10)
state_label = tk.Label(input_frame, text="Enter States (comma-separated):", bg="lightblue")
state_label.grid(row=1, column=0, sticky="w", pady=5)
state_entry = tk.Entry(input_frame, width=30)
state_entry.grid(row=1, column=1, pady=5)
alphabet_label = tk.Label(input_frame, text="Enter Alphabet (comma-separated):", bg="lightblue")
alphabet_label.grid(row=2, column=0, sticky="w", pady=5)
alphabet_entry = tk.Entry(input_frame, width=30)
alphabet_entry.grid(row=2, column=1, pady=5)
start_state_label = tk.Label(input_frame, text="Enter Start State:", bg="lightblue")
start_state_label.grid(row=3, column=0, sticky="w", pady=5)
start_state_entry = tk.Entry(input_frame, width=30)
start_state_entry.grid(row=3, column=1, pady=5)
accept_state_label = tk.Label(input_frame, text="Enter Accepting States (comma-separated):", bg="lightblue")
accept_state_label.grid(row=4, column=0, sticky="w", pady=5)
accept_state_entry = tk.Entry(input_frame, width=30)
accept_state_entry.grid(row=4, column=1, pady=5)
transition_label = tk.Label(input_frame, text="Enter DFA Transitions (state,symbol,next_state):", bg="lightblue")
transition_label.grid(row=5, column=0, sticky="w", pady=5)
transition_entry = tk.Entry(input_frame, width=30)
transition_entry.grid(row=5, column=1, pady=5)
input_string_label = tk.Label(input_frame, text="Enter String to Test:", bg="lightblue")
input_string_label.grid(row=6, column=0, sticky="w", pady=5)
input_string_entry = tk.Entry(input_frame, width=30)
input_string_entry.grid(row=6, column=1, pady=5)
convert_button = tk.Button(input_frame, text="Convert DFA to NFA", command=dfa_to_nfa, bg="white", fg="black")
convert_button.grid(row=7, column=0, columnspan=2, pady=10)
simulate_button = tk.Button(input_frame, text="Test String on NFA", command=simulate_nfa, bg="white", fg="black")
simulate_button.grid(row=8, column=0, columnspan=2, pady=10)
output_title = tk.Label(output_frame, text="Output Section", font=("Arial", 14, "bold"), bg="lightgrey")
output_title.grid(row=0, column=0, pady=10)
nfa_diagram_label = tk.Label(output_frame, bg="lightgrey")
nfa_diagram_label.grid(row=1, column=0, pady=10)
result_label = tk.Label(output_frame, text="Result:", font=("Arial", 12), bg="lightgrey")
result_label.grid(row=2, column=0, pady=10)
root.mainloop()

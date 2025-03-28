from flask import Flask, render_template, request, jsonify
import numpy as np
import networkx as nx

app = Flask(__name__)

def is_safe_state(processes, resources, allocation, max_demand, available):
    allocation = np.array(allocation)
    max_demand = np.array(max_demand)
    available = np.array(available)
    need = max_demand - allocation
    work = available.copy()
    finish = [False] * len(processes)
    safe_sequence = []

    while len(safe_sequence) < len(processes):
        allocated = False
        for i in range(len(processes)):
            if not finish[i] and all(need[i, j] <= work[j] for j in range(len(resources))):
                work += allocation[i]
                finish[i] = True
                safe_sequence.append(processes[i])
                allocated = True
        if not allocated:
            return False, []
    return True, safe_sequence

def detect_deadlock(processes, resources, allocation, max_demand, available):
    G = nx.DiGraph()
    
    # Add process and resource nodes
    for p in processes:
        G.add_node(p, color='blue')
    for r in resources:
        G.add_node(r, color='red')

    allocation = np.array(allocation)
    max_demand = np.array(max_demand)
    available = np.array(available)
    need = max_demand - allocation

    # Add edges based on resource allocation and needs
    for i, process in enumerate(processes):
        for j, res in enumerate(resources):
            if need[i][j] > 0 and allocation[i][j] == 0 and available[j] == 0:
                # Process needs a resource but it's not available (waiting edge)
                G.add_edge(process, res)
            if allocation[i][j] > 0:
                # Process is holding a resource (holding edge)
                G.add_edge(res, process)

    # Detect cycles in the resource allocation graph
    try:
        cycle = list(nx.find_cycle(G, orientation='original'))
        return True, cycle
    except nx.NetworkXNoCycle:
        return False, []
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.json
    processes = data['processes']
    resources = data['resources']
    allocation = data['allocation']
    max_demand = data['max_demand']
    available = data['available']

    safe, sequence = is_safe_state(processes, resources, allocation, max_demand, available)
    deadlock, cycle = detect_deadlock(processes, resources, allocation, max_demand, available)

    return jsonify({
        "safe_state": safe,
        "safe_sequence": sequence if safe else [],
        "deadlock_detected": deadlock,
        "deadlock_cycle": cycle if deadlock else []
    })

if __name__ == '__main__':
    app.run(debug=True)

import tkinter as tk                                #Travel Planner with Shortest Path Visualization
from tkinter import ttk, messagebox
import heapq
import networkx as nx
import matplotlib.pyplot as plt

# --------------------------
# Graph Data (City Network)
# --------------------------
graph = {
    'A': {'B': 5, 'C': 10},
    'B': {'A': 5, 'C': 3, 'D': 9},
    'C': {'A': 10, 'B': 3, 'D': 2},
    'D': {'B': 9, 'C': 2, 'E': 6},
    'E': {'D': 6}
}

# --------------------------
# Dijkstra’s Algorithm
# --------------------------
def dijkstra(graph, start, goal):
    pq = [(0, start, [])]
    visited = set()

    while pq:
        (cost, node, path) = heapq.heappop(pq)
        if node in visited:
            continue
        path = path + [node]
        visited.add(node)

        if node == goal:
            return cost, path

        for neighbor, weight in graph.get(node, {}).items():
            if neighbor not in visited:
                heapq.heappush(pq, (cost + weight, neighbor, path))

    return float("inf"), []

# --------------------------
# Function to Draw the Graph
# --------------------------
def draw_graph(graph, path=[]):
    G = nx.Graph()
    for node, edges in graph.items():
        for neighbor, weight in edges.items():
            G.add_edge(node, neighbor, weight=weight)

    pos = nx.spring_layout(G, seed=42)  # fixed layout
    plt.figure(figsize=(6, 4))
    plt.title("Travel Map", fontsize=14)

    # Draw all nodes and edges
    nx.draw_networkx(G, pos, with_labels=True, node_color='lightblue', node_size=1000, font_size=10)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # Highlight shortest path if available
    if path:
        edge_list = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=edge_list, edge_color='red', width=3)

    plt.show()

# --------------------------
# GUI
# --------------------------
class TravelPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Travel Planner with DAA & Map")
        self.root.geometry("420x320")

        ttk.Label(root, text="Travel Planner", font=("Arial", 16, "bold")).pack(pady=10)

        frame = ttk.Frame(root)
        frame.pack(pady=20)

        ttk.Label(frame, text="Start City:").grid(row=0, column=0, padx=10, pady=5)
        ttk.Label(frame, text="Destination:").grid(row=1, column=0, padx=10, pady=5)

        self.start_var = tk.StringVar()
        self.end_var = tk.StringVar()

        cities = list(graph.keys())
        self.start_cb = ttk.Combobox(frame, textvariable=self.start_var, values=cities, state="readonly")
        self.start_cb.grid(row=0, column=1)
        self.end_cb = ttk.Combobox(frame, textvariable=self.end_var, values=cities, state="readonly")
        self.end_cb.grid(row=1, column=1)

        ttk.Button(root, text="Find Shortest Path", command=self.find_path).pack(pady=10)
        ttk.Button(root, text="Show Map", command=self.show_map).pack(pady=5)

        self.result_label = ttk.Label(root, text="", font=("Arial", 12))
        self.result_label.pack(pady=10)

        self.last_path = []

    def find_path(self):
        start = self.start_var.get()
        end = self.end_var.get()

        if not start or not end:
            messagebox.showerror("Error", "Please select both cities!")
            return
        if start == end:
            messagebox.showwarning("Warning", "Start and destination cannot be the same!")
            return

        distance, path = dijkstra(graph, start, end)
        if distance == float("inf"):
            self.result_label.config(text="No path found.")
            self.last_path = []
        else:
            self.result_label.config(text=f"Shortest Path: {' → '.join(path)}\nTotal Distance: {distance}")
            self.last_path = path

    def show_map(self):
        draw_graph(graph, self.last_path)

# --------------------------
# Run App
# --------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = TravelPlannerApp(root)
    root.mainloop()

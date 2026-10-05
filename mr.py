import heapq

def dijkstra(graph, source, target):
    # Step 1: Initialization
    inf = float('inf')
    distances = {node: inf for node in graph}  # Distance dictionary
    distances[source] = 0
    pq = [(0, source)]  # Priority queue (min-heap), storing (distance, node)
    
    # Step 2: Process vertices
    while pq:
        curr_dist, u = heapq.heappop(pq)  # Get node with the smallest distance
        
        # Early stopping condition: If we reach the target node
        if u == target:
            return curr_dist
        
        # If the popped node has a larger distance than the stored one, skip it
        if curr_dist > distances[u]:
            continue
        
        # Step 3: Relax edges
        for v, weight in graph[u].items():
            new_dist = curr_dist + weight
            if new_dist < distances[v]:  # Relaxation condition
                distances[v] = new_dist
                heapq.heappush(pq, (new_dist, v))
    
    # If the target is unreachable
    return -1 if distances[target] == inf else distances[target]

# Example Usage:
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'C': 2, 'D': 5},
    'C': {'D': 1},
    'D': {}
}

source, target = 'A', 'D'
print(dijkstra(graph, source, target))
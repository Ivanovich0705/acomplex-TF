from queue import PriorityQueue
import math
import networkx as nx

def dijkstra(graph: 'networkx.classes.graph.Graph', start: str, end: str) -> 'List':
    def backtrace(prev, start, end):
        node = end
        path = []
        while node != start:
            path.append(node)
            node = prev[node]
        path.append(node)
        path.reverse()
        return path

    def cost(u, v):
        return graph.get_edge_data(u, v).get('weight')

    prev = {}
    dist = {v: math.inf for v in list(nx.nodes(graph))}
    visited = set()
    pq = PriorityQueue()

    dist[start] = 0  # dist from start -> start is zero
    pq.put((dist[start], start))

    while 0 != pq.qsize():
        curr_cost, curr = pq.get()
        visited.add(curr)
        ##print(f'visiting {curr}')
        # look at curr's adjacent nodes
        if dict(graph.adjacency()).get(curr) is not None:
            for neighbor in dict(graph.adjacency()).get(curr):
                # if we found a shorter path
                path = dist[curr] + cost(curr, neighbor)
                if path < dist[neighbor]:
                    # update the distance, we found a shorter one!
                    dist[neighbor] = path
                    # update the previous node to be prev on new shortest path
                    prev[neighbor] = curr
                    # if we haven't visited the neighbor
                    if neighbor not in visited:
                        # insert into priority queue and mark as visited
                        visited.add(neighbor)
                        pq.put((dist[neighbor], neighbor))
                    # otherwise update the entry in the priority queue
                    else:
                        # remove old
                        _ = pq.get((dist[neighbor], neighbor))
                        # insert new
                        pq.put((dist[neighbor], neighbor))

    return backtrace(prev, start, end), dist[end]

import pandas as pd
import random
import heapq
from collections import deque, defaultdict

class Station:
    def __init__(self, name, line):
        self.name = name
        self.line = line
        self.connections = []  # (station, time, type)

    def __repr__(self):
        return f"{self.name} ({self.line})"

class MetroGraph:
    def __init__(self):
        self.stations = {}  # key: (name, line), value: Station object
        self.name_to_stations = defaultdict(list)  # for handling interchanges

    def add_station(self, name, line):
        key = (name, line)
        if key not in self.stations:
            station = Station(name, line)
            self.stations[key] = station
            self.name_to_stations[name].append(station)

    def add_connection(self, from_key, to_key, time, connection_type):
        from_station = self.stations[from_key]
        to_station = self.stations[to_key]
        from_station.connections.append((to_station, time, connection_type))

    def load_data(self, filepath):
        df = pd.read_csv(filepath)

        # Sort stations by Line and Sequence
        df.sort_values(by=['Line', 'Sequence'], inplace=True)

        for _, row in df.iterrows():
            name = row['Station']
            line = row['Line']
            self.add_station(name, line)

        # Connect sequential stations on the same line
        prev_row = None
        for _, row in df.iterrows():
            if prev_row is not None and prev_row['Line'] == row['Line']:
                key1 = (prev_row['Station'], prev_row['Line'])
                key2 = (row['Station'], row['Line'])
                time = random.randint(2, 8)
                self.add_connection(key1, key2, time, 'same_line')
                self.add_connection(key2, key1, time, 'same_line')
            prev_row = row

        # Connect interchanges
        for stations in self.name_to_stations.values():
            for i in range(len(stations)):
                for j in range(i+1, len(stations)):
                    self.add_connection((stations[i].name, stations[i].line), (stations[j].name, stations[j].line), 5, 'interchange')
                    self.add_connection((stations[j].name, stations[j].line), (stations[i].name, stations[i].line), 5, 'interchange')

    def shortest_path(self, start_name, end_name):
        visited = set()
        queue = deque()
        parents = {}

        for start in self.name_to_stations[start_name]:
            queue.append(start)
            visited.add(start)
            parents[start] = None

        while queue:
            current = queue.popleft()
            if current.name == end_name:
                return self._reconstruct_path(parents, current)

            for neighbor, _, _ in current.connections:
                if neighbor not in visited:
                    visited.add(neighbor)
                    parents[neighbor] = current
                    queue.append(neighbor)

        return None

    def fastest_path(self, start_name, end_name):
        times = {}
        parents = {}
        heap = []

        for start in self.name_to_stations[start_name]:
            times[start] = 0
            heapq.heappush(heap, (0, start))
            parents[start] = None

        while heap:
            current_time, current = heapq.heappop(heap)
            if current.name == end_name:
                return self._reconstruct_path(parents, current)

            for neighbor, time, _ in current.connections:
                new_time = current_time + time
                if neighbor not in times or new_time < times[neighbor]:
                    times[neighbor] = new_time
                    parents[neighbor] = current
                    heapq.heappush(heap, (new_time, neighbor))

        return None

    def _reconstruct_path(self, parents, end_station):
        path = []
        while end_station:
            path.append(end_station)
            end_station = parents[end_station]
        path.reverse()
        return path



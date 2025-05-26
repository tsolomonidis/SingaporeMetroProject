

This Python application models the Singapore MRT/LRT metro system as a graph. It allows users to:

- Find the **shortest path** (fewest stops) between two stations.
- Find the **fastest route** (least total travel time).

---

## Features

- Graph-based metro representation using adjacency lists.
- Random transition times (2-8 minutes) between stations on the same line.
- Fixed 5-minute transfer time between lines at interchange stations.
- Two search algorithms:
  - **Breadth-First Search** for shortest path (unweighted).
  - **Dijkstra's Algorithm** for fastest route (weighted).

---

## Installation

1. Clone the repository 
2. Ensure Python 3.7+ is installed.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

1. Download the dataset from Kaggle:
   https://www.kaggle.com/datasets/shengjunlim/singapore-mrt-lrt-stations-with-coordinates

2. Rename the file to `stations.csv` and place it in the same directory as `main.py`.

3. Run the script:

```bash
python main.py
```

4. Modify `main.py` to specify different start and end stations.

---






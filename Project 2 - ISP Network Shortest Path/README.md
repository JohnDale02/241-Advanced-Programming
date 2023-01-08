
# Project 2: Storing, Searching, and Analysing ISP Network Nodes
- Created a ISPNetwork class to hold Network's and their attributes
- Implemented a function __buildGraph__ to load node data from a file and store the graph in a class variable
- Implemented a function __pathExist__ to determine if a path between two routers exists (Using __Breadth-First Search__)
- Implemented a function __buildMST__ to create a __Minimum Spanning Tree__ based on path cost between routers
- Implemented a function __findForwardingPath__ to return __minimum cost__ between routers
- Implemented a function __findPathMaxWeight__ to choose the path with the smallest individual link weight (Using modified __Dijkstra's Algorithm__)

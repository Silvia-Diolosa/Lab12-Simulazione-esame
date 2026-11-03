import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self.idMap = {}



    def getAllRatings(self):
        return DAO.getAllRatings()


    def buildGraph(self, r1, r2):
        self._graph.clear()
        nodes = DAO.getAllNodes(r1, r2)
        for node in nodes:
            self.idMap[node.id] = node


        self._graph.add_nodes_from(nodes)

        edges_quasi = DAO.getAllEdges(r1, r2, self.idMap)
        for edge in edges_quasi:
            u = edge[0]
            v = edge[1]
            incasso = edge[2]
            incasso = incasso.replace("$", "").replace(",", "").strip()
            try:
                incassoInt = int(incasso)
            except ValueError:
                continue
            if (u, v) in self._graph.edges:
                self._graph[u][v]["weight"] += incassoInt
            else:
                self._graph.add_edge(u, v, weight=incassoInt)


    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)


    def getAllEdges(self):
        edges = list(self._graph.edges(data=True))
        edges.sort(key=lambda x: x[2]["weight"], reverse=True)
        return edges

    def getAllNodes(self):
        return list(self._graph.nodes)


    def compConn(self):
        nComConn = nx.number_connected_components(self._graph)

        components = list(nx.connected_components(self._graph))

        largest = max(components, key=len)

        return nComConn, largest



    def getBestPath(self):
        self.bestPath = []
        self.parziale = []

        nodes = self.getAllNodes()
        for partenza in nodes:
            self.parziale.append(partenza)
            self.ricorsione(partenza, self.parziale)
            self.parziale.pop()

        return self.bestPath



    def ricorsione(self, partenza, parziale):

        # caso terminale
        if len(parziale) > len(self.bestPath):
            self.bestPath = copy.deepcopy(self.parziale)

        # caso terminale
        for n in self._graph.neighbors(partenza):
            if n not in parziale:
                if self.condizione(n, parziale):
                    parziale.append(n)
                    self.ricorsione(n, parziale)
                    parziale.pop()

        # prendo il primo nodo:
        # lo appendo
        # prendo i suoi vicini
        #per ogni vicino lo appendo
        # faccio la ricorsione
        # lo tolgo

        # poi prendo il secondo nodo



    def condizione(self, n, parziale):
        if parziale[-1].date_of_birth < n.date_of_birth: # decrescente: dal piu vecchio al più giovane
            return True                                   # quindi da date più piccole a più grandi
        return False





    # OPPURE SOLUZIONE PROF:
    def getBestPath2(self):

        self._bestPath = []

        for start in self._graph.nodes():
            partial = [start]
            self._ricorsione(partial)

        return self._bestPath

    def ricorsione2(self, partial):

        if len(partial) > len(self._bestPath):
            self._bestPath = list(partial)

        current = partial[-1]
        # L’ultimo nodo del cammino: da qui si cerca di proseguire.

        for _, successor in self._graph.edges(current):

            # vincolo: età decrescente
            if successor not in partial and successor.birth_date > current.birth_date:
                partial.append(successor)

                self._ricorsione(partial)

                partial.pop()
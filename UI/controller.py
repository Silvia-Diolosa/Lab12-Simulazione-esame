import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDsRating(self):
        ratings = self._model.getAllRatings()
        for r in ratings:
            self._view._ddrating1.options.append(ft.dropdown.Option(r))
            self._view._ddrating2.options.append(ft.dropdown.Option(r))


    def handleCreaGrafo(self, e):
        if self._view._ddrating1.value is None or self._view._ddrating2.value is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Selezionare un valore dal menu."))
            return

        self._model.buildGraph(self._view._ddrating1.value, self._view._ddrating2.value)
        nNodi, nArchi = self._model.getGraphDetails()

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text("Grafo correttamente creato.", color="green"))
        self._view.txt_result.controls.append(
            ft.Text(f"Nodi: {nNodi}, Archi: {nArchi}"))

        edges = self._model.getAllEdges()
        best5 = edges[0:5]
        for e in best5:
            self._view.txt_result.controls.append(ft.Text(f" {e[0].name}-- {e[1].name}: {e[2]["weight"]}"))


        nCompMax, compMax = self._model.compConn()
        self._view.txt_result.controls.append(ft.Text(f"il grafo ha {nCompMax} componenti connesse."))

        self._view.txt_result.controls.append(ft.Text(f"la componente connesse maggiore ha {len(compMax)} archi"))

        for e in compMax:
            self._view.txt_result.controls.append(ft.Text(e))



        self._view.update_page()


    def handleCammino(self, e):
        bestPath = self._model.getBestPath()

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Best path lunghezza: {len(bestPath)}"))
        for e in bestPath:
            self._view.txt_result.controls.append(ft.Text(e))

        self._view.update_page()
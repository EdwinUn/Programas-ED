import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx

class GrafoAPI:
    def __init__(self):
        self.vertices_dict = {} # (id: datos_objeto)
        self.aristas_dict = {} # (id: (u, v, datos_objeto, is_directed))
        self.vertice_counter = 0
        self.arista_counter = 0

    # Operaciones generales (image_0.png)
    def numVertices(self):
        return len(self.vertices_dict)

    def numAristas(self):
        return len(self.aristas_dict)

    def vertices(self):
        return list(self.vertices_dict.keys())

    def aristas(self):
        return list(self.aristas_dict.keys())

    def grado(self, v):
        # Grado total para DiGraph (entrante + saliente)
        if v not in self.vertices_dict: return -1
        degree = 0
        for e_id, (u, w, _, is_directed) in self.aristas_dict.items():
            if u == v or w == v:
                degree += 1
        return degree

    def verticesAdyacentes(self, v):
        # Todos los vecinos
        if v not in self.vertices_dict: return []
        neighbors = set()
        for e_id, (u, w, _, is_directed) in self.aristas_dict.items():
            if u == v: neighbors.add(w)
            elif w == v: neighbors.add(u)
        return list(neighbors)

    def aristasIncidentes(self, v):
        # Aristas que tocan el nodo (entrantes y salientes)
        aristas_ids = []
        for e_id, (u, w, _, is_directed) in self.aristas_dict.items():
            if u == v or w == v:
                aristas_ids.append(e_id)
        return aristas_ids

    def verticesFinales(self, e):
        if e in self.aristas_dict:
            u, v, _, _ = self.aristas_dict[e]
            return [u, v]
        return None

    def opuesto(self, v, e):
        if e in self.aristas_dict:
            u, w, _, _ = self.aristas_dict[e]
            if u == v: return w
            elif w == v: return u
        return None

    def esAdyacente(self, v, w):
        if v not in self.vertices_dict or w not in self.vertices_dict: return False
        for e_id, (u1, v1, _, _) in self.aristas_dict.items():
             if (u1 == v and v1 == w) or (u1 == w and v1 == v):
                 return True
        return False


    # Operaciones con aristas dirigidas (image_1.png)
    def aristasDirigidas(self):
        return [e_id for e_id, (_, _, _, is_directed) in self.aristas_dict.items() if is_directed]

    def aristasNodirigidas(self):
        return [e_id for e_id, (_, _, _, is_directed) in self.aristas_dict.items() if not is_directed]

    def gradoEnt(self, v):
        if v not in self.vertices_dict: return -1
        degree = 0
        for e_id, (u, w, _, is_directed) in self.aristas_dict.items():
            if w == v and is_directed: degree += 1
            elif (u == v or w == v) and not is_directed: degree += 1
        return degree

    def gradoSalida(self, v):
        if v not in self.vertices_dict: return -1
        degree = 0
        for e_id, (u, w, _, is_directed) in self.aristas_dict.items():
            if u == v and is_directed: degree += 1
            elif (u == v or w == v) and not is_directed: degree += 1
        return degree

    def aristasIncidentesEnt(self, v):
        aristas_ids = []
        for e_id, (u, w, _, is_directed) in self.aristas_dict.items():
            if w == v and is_directed: aristas_ids.append(e_id)
            elif (u == v or w == v) and not is_directed: aristas_ids.append(e_id)
        return aristas_ids

    def aristasIncidentesSal(self, v):
        aristas_ids = []
        for e_id, (u, w, _, is_directed) in self.aristas_dict.items():
            if u == v and is_directed: aristas_ids.append(e_id)
            elif (u == v or w == v) and not is_directed: aristas_ids.append(e_id)
        return aristas_ids

    def verticesAdyacentesEnt(self, v):
        if v not in self.vertices_dict: return []
        preds = set()
        for e_id, (u, w, _, is_directed) in self.aristas_dict.items():
            if w == v and is_directed: preds.add(u)
            elif (u == v or w == v) and not is_directed: preds.add(u if w == v else w)
        return list(preds)

    def verticesAdyacentesSal(self, v):
        if v not in self.vertices_dict: return []
        succs = set()
        for e_id, (u, w, _, is_directed) in self.aristas_dict.items():
            if u == v and is_directed: succs.add(w)
            elif (u == v or w == v) and not is_directed: succs.add(u if w == v else w)
        return list(succs)

    def destino(self, e):
        if e in self.aristas_dict:
            u, w, _, is_directed = self.aristas_dict[e]
            if is_directed: return w
        return None

    def origen(self, e):
        if e in self.aristas_dict:
            u, w, _, is_directed = self.aristas_dict[e]
            if is_directed: return u
        return None

    def esDirigida(self, e):
        if e in self.aristas_dict:
            return self.aristas_dict[e][3]
        return False


    # Operaciones para actualizar grafos (image_2.png)
    def insertaArista(self, v, w, o):
        if v in self.vertices_dict and w in self.vertices_dict:
            e_id = self.arista_counter
            self.arista_counter += 1
            self.aristas_dict[e_id] = (v, w, o, False)
            return e_id
        return -1

    def insertaAristaDirigida(self, v, w, o):
        if v in self.vertices_dict and w in self.vertices_dict:
            e_id = self.arista_counter
            self.arista_counter += 1
            self.aristas_dict[e_id] = (v, w, o, True)
            return e_id
        return -1

    def insertaVertice(self, o):
        v_id = self.vertice_counter
        self.vertice_counter += 1
        self.vertices_dict[v_id] = o
        return v_id

    def eliminaVertice(self, v):
        if v in self.vertices_dict:
            # Eliminar aristas incidentes de self.aristas_dict
            edges_to_remove = [e_id for e_id, (u, w, _, _) in self.aristas_dict.items() if u == v or w == v]
            for e_id in edges_to_remove:
                del self.aristas_dict[e_id]
            # Eliminar nodo
            del self.vertices_dict[v]
            return True
        return False

    def eliminaArista(self, e):
        if e in self.aristas_dict:
            del self.aristas_dict[e]
            return True
        return False

    def convierteNoDirigida(self, e):
        if e in self.aristas_dict:
            u, v, o, is_directed = self.aristas_dict[e]
            if is_directed:
                self.aristas_dict[e] = (u, v, o, False)
                return True
        return False

    def invierteDireccion(self, e):
        if e in self.aristas_dict:
            u, v, o, is_directed = self.aristas_dict[e]
            if is_directed:
                # Actualizar dict con el nuevo origen y destino
                self.aristas_dict[e] = (v, u, o, True)
                return True
        return False

    def asignaDireccionDesde(self, e, v):
        if e in self.aristas_dict:
            u, w, o, is_directed = self.aristas_dict[e]
            if u != v and w != v: return False # v no es un extremo
            if not is_directed:
                # Arista no dirigida (u, w). Forzar (v, opuesto)
                opposite = u if w == v else w
                self.aristas_dict[e] = (v, opposite, o, True)
                return True
        return False

    def asignaDireccionA(self, e, v):
        if e in self.aristas_dict:
            u, w, o, is_directed = self.aristas_dict[e]
            if u != v and w != v: return False # v no es un extremo
            if not is_directed:
                # Arista no dirigida (u, w). Forzar (opuesto, v)
                opposite = u if w == v else w
                self.aristas_dict[e] = (opposite, v, o, True)
                return True
        return False


class GrafoVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Grafo API")
        self.grafo = GrafoAPI()

        # Layout principal
        self.control_frame = tk.Frame(root, width=350)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.setup_controls()
        self.setup_canvas()

    def setup_controls(self):
        # Campos de entrada
        tk.Label(self.control_frame, text="Inputs:", font=("Arial", 12, "bold")).pack(pady=5)
        self.create_labeled_entry(self.control_frame, "ID Vértice 1 (v1):", "v1_entry")
        self.create_labeled_entry(self.control_frame, "ID Vértice 2 (v2/w):", "v2_entry")
        self.create_labeled_entry(self.control_frame, "ID Arista (e):", "e_entry")
        self.create_labeled_entry(self.control_frame, "Dato Objeto (o):", "obj_entry")


        # Botones de Acción
        update_frame = tk.LabelFrame(self.control_frame, text="Actualizar Grafo")
        update_frame.pack(fill=tk.X, padx=5, pady=5)
        self.add_button(update_frame, "Inserta Vértice(o)", self.op_insertaVertice)
        self.add_button(update_frame, "Inserta Arista No Dir(v1, v2, o)", self.op_insertaArista)
        self.add_button(update_frame, "Inserta Arista Dir(v1, v2, o)", self.op_insertaAristaDirigida)
        self.add_button(update_frame, "Elimina Vértice(v1)", self.op_eliminaVertice)
        self.add_button(update_frame, "Elimina Arista(e)", self.op_eliminaArista)
        self.add_button(update_frame, "Convierte No Dir(e)", self.op_convierteNoDirigida)
        self.add_button(update_frame, "Invierte Dir(e)", self.op_invierteDireccion)
        self.add_button(update_frame, "Asigna Dir Desde(e, v1)", self.op_asignaDireccionDesde)
        self.add_button(update_frame, "Asigna Dir A(e, v1)", self.op_asignaDireccionA)

        general_frame = tk.LabelFrame(self.control_frame, text="Operaciones Generales")
        general_frame.pack(fill=tk.X, padx=5, pady=5)
        self.add_button(general_frame, "numVertices()", self.op_numVertices)
        self.add_button(general_frame, "numAristas()", self.op_numAristas)
        self.add_button(general_frame, "vertices()", self.op_vertices)
        self.add_button(general_frame, "aristas()", self.op_aristas)
        self.add_button(general_frame, "grado(v1)", self.op_grado)
        self.add_button(general_frame, "verts Ady(v1)", self.op_verticesAdyacentes)
        self.add_button(general_frame, "arts Inc(v1)", self.op_aristasIncidentes)
        self.add_button(general_frame, "verts Finales(e)", self.op_verticesFinales)
        self.add_button(general_frame, "opuesto(v1, e)", self.op_opuesto)
        self.add_button(general_frame, "es Ady(v1, v2)", self.op_esAdyacente)

        directed_frame = tk.LabelFrame(self.control_frame, text="Aristas Dirigidas")
        directed_frame.pack(fill=tk.X, padx=5, pady=5)
        self.add_button(directed_frame, "arts Dirigidas()", self.op_aristasDirigidas)
        self.add_button(directed_frame, "arts No Dir()", self.op_aristasNodirigidas)
        self.add_button(directed_frame, "grado Ent(v1)", self.op_gradoEnt)
        self.add_button(directed_frame, "grado Sal(v1)", self.op_gradoSalida)
        self.add_button(directed_frame, "arts Inc Ent(v1)", self.op_aristasIncidentesEnt)
        self.add_button(directed_frame, "arts Inc Sal(v1)", self.op_aristasIncidentesSal)
        self.add_button(directed_frame, "verts Ady Ent(v1)", self.op_verticesAdyacentesEnt)
        self.add_button(directed_frame, "verts Ady Sal(v1)", self.op_verticesAdyacentesSal)
        self.add_button(directed_frame, "destino(e)", self.op_destino)
        self.add_button(directed_frame, "origen(e)", self.op_origen)
        self.add_button(directed_frame, "es Dirigida(e)", self.op_esDirigida)

        tk.Label(self.control_frame, text="Resultados:", font=("Arial", 10, "italic")).pack(pady=(10, 0))
        self.result_text = tk.Text(self.control_frame, height=5, width=40)
        self.result_text.pack(pady=5)

    def create_labeled_entry(self, parent, label_text, attr_name):
        frame = tk.Frame(parent)
        frame.pack(fill=tk.X, pady=2)
        tk.Label(frame, text=label_text, width=20, anchor=tk.W).pack(side=tk.LEFT)
        entry = tk.Entry(frame, width=15)
        entry.pack(side=tk.LEFT)
        setattr(self, attr_name, entry)

    def add_button(self, parent, text, command):
        tk.Button(parent, text=text, command=command, font=("Arial", 8)).pack(anchor=tk.W, fill=tk.X)

    def setup_canvas(self):
        self.figure, self.ax = plt.subplots(figsize=(7, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.canvas_frame)
        # Cambio solucionado: get_tk_widget()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.draw_graph()

    def draw_graph(self):
        self.ax.clear()
        
        # Crear grafo temporal de visualización
        viz_graph = nx.DiGraph() 

        for v_id, o in self.grafo.vertices_dict.items():
            viz_graph.add_node(v_id, label=f"{v_id}\n'{o}'")

        directed_edges = []
        undirected_pairs = []
        seen_undirected = set()

        for e_id, (u, v, o, is_directed) in self.grafo.aristas_dict.items():
            # Cambio solucionado: usamos 'data_obj' en vez de 'weight'
            viz_graph.add_edge(u, v, data_obj=o, edge_id=e_id, is_directed=is_directed)
            if is_directed:
                directed_edges.append((u, v))
            else:
                pair = tuple(sorted((u, v)))
                if pair not in seen_undirected:
                    undirected_pairs.append((u, v))
                    seen_undirected.add(pair)
                # Cambio solucionado: usamos 'data_obj' en vez de 'weight'
                viz_graph.add_edge(v, u, data_obj=o, edge_id=e_id, is_directed=is_directed)

        # Usamos weight=None para asegurar que Networkx no busque la propiedad weight que borramos
        pos = nx.spring_layout(viz_graph, weight=None, k=1)

        # Dibujar nodos
        nx.draw_networkx_nodes(viz_graph, pos, ax=self.ax, node_color='skyblue', node_size=800, edgecolors='black')
        
        # Dibujar etiquetas
        labels = nx.get_node_attributes(viz_graph, 'label')
        nx.draw_networkx_labels(viz_graph, pos, labels, ax=self.ax, font_size=10, font_weight='bold')

        # Dibujar aristas dirigidas
        nx.draw_networkx_edges(viz_graph, pos, edgelist=directed_edges, ax=self.ax, edge_color='black', arrows=True, arrowstyle='-|>', arrowsize=20)
        
        # Dibujar aristas no dirigidas
        nx.draw_networkx_edges(viz_graph, pos, edgelist=undirected_pairs, ax=self.ax, edge_color='gray', style='solid', arrows=False, width=2)

        # Etiquetas de aristas
        edge_labels = {}
        for (u, v, d) in viz_graph.edges(data=True):
            if d['is_directed']:
                # Cambio solucionado: llamamos a 'data_obj'
                edge_labels[(u, v)] = f"e{d['edge_id']} : '{d['data_obj']}'"
        for (u, v) in undirected_pairs:
            for e_id, (u1, v1, o, is_directed) in self.grafo.aristas_dict.items():
                if not is_directed and ((u1 == u and v1 == v) or (u1 == v and v1 == u)):
                     edge_labels[(u, v)] = f"e{e_id} : '{o}'"
                     break

        nx.draw_networkx_edge_labels(viz_graph, pos, edge_labels, ax=self.ax, font_color='red', font_size=8)

        self.canvas.draw()

    # Métodos auxiliares de entrada
    def get_v1(self): return int(self.v1_entry.get()) if self.v1_entry.get().isdigit() else None
    def get_v2(self): return int(self.v2_entry.get()) if self.v2_entry.get().isdigit() else None
    def get_e(self): return int(self.e_entry.get()) if self.e_entry.get().isdigit() else None
    def get_obj(self): return self.obj_entry.get()

    def update_result(self, text):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(1.0, text)


    # --- Métodos de manejo de operaciones ---

    def op_insertaVertice(self):
        v_id = self.grafo.insertaVertice(self.get_obj())
        self.update_result(f"Vértice {v_id} insertado.")
        self.draw_graph()

    def op_insertaArista(self):
        v1, v2, obj = self.get_v1(), self.get_v2(), self.get_obj()
        if v1 is not None and v2 is not None:
            e_id = self.grafo.insertaArista(v1, v2, obj)
            if e_id != -1:
                self.update_result(f"Arista no dir {e_id} ({v1}-{v2}) insertada.")
                self.draw_graph()
            else:
                messagebox.showerror("Error", "Los vértices no existen.")
        else:
             messagebox.showerror("Error", "IDs de vértice inválidos.")

    def op_insertaAristaDirigida(self):
        v1, v2, obj = self.get_v1(), self.get_v2(), self.get_obj()
        if v1 is not None and v2 is not None:
            e_id = self.grafo.insertaAristaDirigida(v1, v2, obj)
            if e_id != -1:
                self.update_result(f"Arista dir {e_id} ({v1}->{v2}) insertada.")
                self.draw_graph()
            else:
                messagebox.showerror("Error", "Los vértices no existen.")
        else:
             messagebox.showerror("Error", "IDs de vértice inválidos.")

    def op_eliminaVertice(self):
        v1 = self.get_v1()
        if v1 is not None:
            if self.grafo.eliminaVertice(v1):
                self.update_result(f"Vértice {v1} eliminado.")
                self.draw_graph()
            else:
                self.update_result(f"Error: vértice {v1} no encontrado.")
        else:
            messagebox.showerror("Error", "ID de vértice inválido.")

    def op_eliminaArista(self):
        e_id = self.get_e()
        if e_id is not None:
            if self.grafo.eliminaArista(e_id):
                self.update_result(f"Arista {e_id} eliminada.")
                self.draw_graph()
            else:
                self.update_result(f"Error: arista {e_id} no encontrada.")
        else:
            messagebox.showerror("Error", "ID de arista inválido.")

    def op_convierteNoDirigida(self):
        e_id = self.get_e()
        if e_id is not None:
            if self.grafo.convierteNoDirigida(e_id):
                self.update_result(f"Arista {e_id} convertida a no dirigida.")
                self.draw_graph()
            else:
                self.update_result(f"Error: arista no encontrada o ya no dirigida.")
        else:
             messagebox.showerror("Error", "ID de arista inválido.")

    def op_invierteDireccion(self):
        e_id = self.get_e()
        if e_id is not None:
            if self.grafo.invierteDireccion(e_id):
                self.update_result(f"Dirección de arista {e_id} invertida.")
                self.draw_graph()
            else:
                self.update_result(f"Error: arista no encontrada o no dirigida.")
        else:
             messagebox.showerror("Error", "ID de arista inválido.")

    def op_asignaDireccionDesde(self):
        e_id, v1 = self.get_e(), self.get_v1()
        if e_id is not None and v1 is not None:
            if self.grafo.asignaDireccionDesde(e_id, v1):
                self.update_result(f"Arista {e_id} asignada como saliente desde {v1}.")
                self.draw_graph()
            else:
                self.update_result(f"Error: arista o vértice no válidos.")
        else:
             messagebox.showerror("Error", "IDs de arista o vértice inválidos.")

    def op_asignaDireccionA(self):
        e_id, v1 = self.get_e(), self.get_v1()
        if e_id is not None and v1 is not None:
            if self.grafo.asignaDireccionA(e_id, v1):
                self.update_result(f"Arista {e_id} asignada como entrante a {v1}.")
                self.draw_graph()
            else:
                self.update_result(f"Error: arista o vértice no válidos.")
        else:
             messagebox.showerror("Error", "IDs de arista o vértice inválidos.")

    def op_numVertices(self):
        self.update_result(f"Número de vértices: {self.grafo.numVertices()}")

    def op_numAristas(self):
        self.update_result(f"Número de aristas: {self.grafo.numAristas()}")

    def op_vertices(self):
        self.update_result(f"Lista de vértices de G: {self.grafo.vertices()}")

    def op_aristas(self):
        self.update_result(f"Lista de aristas de G: {self.grafo.aristas()}")

    def op_grado(self):
        v1 = self.get_v1()
        if v1 is not None:
            self.update_result(f"Grado de v{v1}: {self.grafo.grado(v1)}")
        else:
            messagebox.showerror("Error", "ID de vértice inválido.")

    def op_verticesAdyacentes(self):
        v1 = self.get_v1()
        if v1 is not None:
            self.update_result(f"Vértices adyacentes a v{v1}: {self.grafo.verticesAdyacentes(v1)}")
        else:
            messagebox.showerror("Error", "ID de vértice inválido.")

    def op_aristasIncidentes(self):
        v1 = self.get_v1()
        if v1 is not None:
            self.update_result(f"Aristas incidentes en v{v1}: {self.grafo.aristasIncidentes(v1)}")
        else:
            messagebox.showerror("Error", "ID de vértice inválido.")

    def op_verticesFinales(self):
        e_id = self.get_e()
        if e_id is not None:
            self.update_result(f"Vértices finales de e{e_id}: {self.grafo.verticesFinales(e_id)}")
        else:
            messagebox.showerror("Error", "ID de arista inválido.")

    def op_opuesto(self):
        v1, e_id = self.get_v1(), self.get_e()
        if v1 is not None and e_id is not None:
            self.update_result(f"Extremo opuesto a v{v1} en e{e_id}: {self.grafo.opuesto(v1, e_id)}")
        else:
            messagebox.showerror("Error", "IDs de vértice o arista inválidos.")

    def op_esAdyacente(self):
        v1, v2 = self.get_v1(), self.get_v2()
        if v1 is not None and v2 is not None:
            res = "verdadero" if self.grafo.esAdyacente(v1, v2) else "falso"
            self.update_result(f"¿Son adyacentes v{v1} y v{v2}? {res}")
        else:
            messagebox.showerror("Error", "IDs de vértice inválidos.")

    def op_aristasDirigidas(self):
        self.update_result(f"Aristas dirigidas: {self.grafo.aristasDirigidas()}")

    def op_aristasNodirigidas(self):
        self.update_result(f"Aristas no dirigidas: {self.grafo.aristasNodirigidas()}")

    def op_gradoEnt(self):
        v1 = self.get_v1()
        if v1 is not None:
            self.update_result(f"Grado de entrada de v{v1}: {self.grafo.gradoEnt(v1)}")
        else:
            messagebox.showerror("Error", "ID de vértice inválido.")

    def op_gradoSalida(self):
        v1 = self.get_v1()
        if v1 is not None:
            self.update_result(f"Grado de salida de v{v1}: {self.grafo.gradoSalida(v1)}")
        else:
            messagebox.showerror("Error", "ID de vértice inválido.")

    def op_aristasIncidentesEnt(self):
        v1 = self.get_v1()
        if v1 is not None:
            self.update_result(f"Aristas incidentes entrantes en v{v1}: {self.grafo.aristasIncidentesEnt(v1)}")
        else:
            messagebox.showerror("Error", "ID de vértice inválido.")

    def op_aristasIncidentesSal(self):
        v1 = self.get_v1()
        if v1 is not None:
            self.update_result(f"Aristas incidentes salientes desde v{v1}: {self.grafo.aristasIncidentesSal(v1)}")
        else:
            messagebox.showerror("Error", "ID de vértice inválido.")

    def op_verticesAdyacentesEnt(self):
        v1 = self.get_v1()
        if v1 is not None:
            self.update_result(f"Vértices adyacentes entrantes a v{v1}: {self.grafo.verticesAdyacentesEnt(v1)}")
        else:
            messagebox.showerror("Error", "ID de vértice inválido.")

    def op_verticesAdyacentesSal(self):
        v1 = self.get_v1()
        if v1 is not None:
            self.update_result(f"Vértices adyacentes salientes de v{v1}: {self.grafo.verticesAdyacentesSal(v1)}")
        else:
            messagebox.showerror("Error", "ID de vértice inválido.")

    def op_destino(self):
        e_id = self.get_e()
        if e_id is not None:
            self.update_result(f"Destino de e{e_id}: {self.grafo.destino(e_id)}")
        else:
            messagebox.showerror("Error", "ID de arista inválido.")

    def op_origen(self):
        e_id = self.get_e()
        if e_id is not None:
            self.update_result(f"Origen de e{e_id}: {self.grafo.origen(e_id)}")
        else:
            messagebox.showerror("Error", "ID de arista inválido.")

    def op_esDirigida(self):
        e_id = self.get_e()
        if e_id is not None:
            res = "verdadero" if self.grafo.esDirigida(e_id) else "falso"
            self.update_result(f"¿Es dirigida e{e_id}? {res}")
        else:
            messagebox.showerror("Error", "ID de arista inválido.")


if __name__ == "__main__":
    root = tk.Tk()
    app = GrafoVisualizerApp(root)
    
    # Crear un grafo de ejemplo para empezar
    v1 = app.grafo.insertaVertice("Nodo 1")
    v2 = app.grafo.insertaVertice("Nodo 2")
    v3 = app.grafo.insertaVertice("Nodo 3")
    app.grafo.insertaArista(v1, v2, "no dirigida")
    app.grafo.insertaAristaDirigida(v1, v3, "dirigida")
    app.grafo.insertaAristaDirigida(v3, v2, "dirigida")
    app.draw_graph()
    
    root.mainloop()
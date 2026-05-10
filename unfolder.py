import trimesh
import networkx as nx

def main():
    print("=== Papercraft Generator: Тест 01 ===")
    
    # 1. Генерируем простую 3D-модель (Куб 10x10x10 см)
    # В будущем здесь будет загрузка .obj файла пользователя
    mesh = trimesh.creation.box(extents=[10, 10, 10])
    print(f"[+] 3D-модель загружена. Граней: {len(mesh.faces)}, Вершин: {len(mesh.vertices)}")

    # 2. Строим граф смежности граней
    # Каждая грань - это узел (node), а общее ребро между гранями - связь (edge)
    face_adjacency = mesh.face_adjacency
    graph = nx.Graph()
    graph.add_edges_from(face_adjacency)
    print(f"[+] Граф смежности построен. Всего связей между гранями: {graph.number_of_edges()}")

    # 3. Находим минимальное остовное дерево (MST)
    # MST оставит ровно столько связей (сгибов), чтобы детали не развалились, 
    # но при этом куб можно было развернуть на плоскости без разрывов.
    mst = nx.minimum_spanning_tree(graph)
    print(f"[+] Остовное дерево (линии сгиба) рассчитано. Ребер для сгиба: {mst.number_of_edges()}")

    # 4. Вычисляем линии разреза
    # Все ребра, которые не вошли в MST, становятся местами, где нужно резать бумагу
    cut_edges = graph.number_of_edges() - mst.number_of_edges()
    print(f"[+] Линий для разреза ножницами: {cut_edges}")

    # Сохраним 3D-модель локально, чтобы убедиться, что она существует
    mesh.export('test_cube.obj')
    print("\n[!] Модель сохранена в test_cube.obj")

if __name__ == "__main__":
    main()
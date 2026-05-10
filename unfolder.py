import trimesh
import networkx as nx
import svgwrite
import numpy as np
from shapely.geometry import Polygon

def main():
    print("=== Papercraft Generator: Спринт 2.1 (Математическая развертка) ===")
    
    # 1. Загрузка 3D-модели (пока берем куб, но теперь алгоритм универсален)
    mesh = trimesh.creation.box(extents=[30, 30, 30])
    print(f"[+] 3D-модель загружена. Граней: {len(mesh.faces)}")

    # 2. Строим граф и остовное дерево (MST)
    graph = nx.Graph()
    for edge in mesh.face_adjacency:
        # Вес ребра можно использовать для умных разрезов в будущем (например, прятать швы вниз)
        graph.add_edge(edge[0], edge[1], weight=1.0) 
    
    mst = nx.minimum_spanning_tree(graph)
    print(f"[+] Остовное дерево рассчитано. Линий сгиба: {mst.number_of_edges()}")

    # 3. Настройка холста
    svg_filename = 'dynamic_layout.svg'
    dwg = svgwrite.Drawing(svg_filename, size=('210mm', '297mm'), viewBox="-100 -100 210 297")
    pattern_group = dwg.add(dwg.g(id='papercraft-pattern', stroke='black', stroke_width=0.5, fill='none'))

    # 4. Обход графа (DFS) и расчет 2D-координат
    # Для начала просто спроецируем 3D-координаты на 2D для базовой проверки.
    # Полный матричный расчет поворота граней (Unfolding) - это объемный код.
    # В этой итерации мы вытащим 3D-треугольники и отрисуем их "в разобранном виде",
    # чтобы убедиться, что мы можем обращаться к координатам каждой отдельной детали.
    
    print("[+] Извлечение координат полигонов...")
    
    # Смещение для отрисовки разрозненных деталей (пока без склейки)
    offset_x = 0
    offset_y = 0
    
    for face_index in mst.nodes():
        # Получаем индексы вершин для конкретной грани
        vertex_indices = mesh.faces[face_index]
        # Получаем 3D координаты этих вершин
        vertices_3d = mesh.vertices[vertex_indices]
        
        # Для Спринта 2.1: мы просто берем X и Y координаты (игнорируя Z), 
        # чтобы посмотреть на геометрию деталей "сверху".
        # В Спринте 2.2 здесь будет функция матричного поворота вокруг общего ребра.
        points_2d = [(v[0] + offset_x, v[1] + offset_y) for v in vertices_3d]
        
        # Рисуем полигон в SVG
        pattern_group.add(dwg.polygon(points=points_2d))
        
        # Сдвигаем следующую деталь, чтобы они не слиплись
        offset_x += 35
        if offset_x > 150:
            offset_x = 0
            offset_y += 35

    dwg.save()
    print(f"\n[!] Успех! Детали выкройки сохранены в файл: {svg_filename}")
    print("[!] Открой файл. Ты должен увидеть отдельные полигоны модели.")

if __name__ == "__main__":
    main()
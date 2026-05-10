import trimesh
import networkx as nx
import svgwrite

def main():
    print("=== Papercraft Generator: Спринт 1.4 (Экспорт в SVG) ===")
    
    # 1. Загрузка 3D-модели
    mesh = trimesh.creation.box(extents=[10, 10, 10])
    print(f"[+] 3D-модель загружена. Граней: {len(mesh.faces)}")

    # 2. Математика: Граф и Остовное дерево (MST)
    graph = nx.Graph()
    graph.add_edges_from(mesh.face_adjacency)
    mst = nx.minimum_spanning_tree(graph)
    print(f"[+] Остовное дерево рассчитано. Линий сгиба: {mst.number_of_edges()}")

    # 3. Настройка холста для выкройки (Лист А4)
    # Размер А4: 210 x 297 мм
    svg_filename = 'model_layout.svg'
    dwg = svgwrite.Drawing(svg_filename, size=('210mm', '297mm'), viewBox="0 0 210 297")
    
    # Создаем группу для деталей, чтобы потом можно было легко менять масштаб
    pattern_group = dwg.add(dwg.g(id='papercraft-pattern'))

    # 4. Временная генерация плоской выкройки для проверки пайплайна
    # В Спринте 2 здесь будет алгоритм DFS-обхода графа mst, который 
    # математически "положит" каждую 3D-грань на эту 2D-плоскость.
    print("[+] Генерация векторных контуров...")
    
    face_size = 30 # размер одной грани куба в мм на бумаге
    start_x, start_y = 90, 50 # начальная точка рисования на листе
    
    # Функция для отрисовки одного квадрата (грани)
    def draw_face(x, y):
        # Рисуем сплошную линию (линия реза)
        pattern_group.add(dwg.rect(insert=(x, y), size=(face_size, face_size), 
                                   fill='white', stroke='black', stroke_width=0.5))

    # Рисуем классическую развертку куба ("крест")
    # Центральная вертикаль
    draw_face(start_x, start_y)
    draw_face(start_x, start_y + face_size)
    draw_face(start_x, start_y + face_size * 2)
    draw_face(start_x, start_y + face_size * 3)
    # Боковые "крылья"
    draw_face(start_x - face_size, start_y + face_size)
    draw_face(start_x + face_size, start_y + face_size)

    # 5. Сохранение файла
    dwg.save()
    print(f"\n[!] Успех! Выкройка сохранена в файл: {svg_filename}")
    print("[!] Открой этот файл в браузере (Chrome/Firefox), чтобы посмотреть результат.")

if __name__ == "__main__":
    main()
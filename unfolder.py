import svgwrite
import math

def main():
    print("=== Papercraft Generator: Спринт 2.3 (Исправленные клапаны) ===")
    
    svg_filename = 'unfolded_with_tabs_fixed.svg'
    dwg = svgwrite.Drawing(svg_filename, size=('210mm', '297mm'), viewBox="-100 -150 300 350")
    pattern_group = dwg.add(dwg.g(id='papercraft-pattern', stroke='black', stroke_width=0.5, fill='none'))
    
    face_size = 40 
    
    # 1. Сгенерированные координаты креста (наша 2D-развертка)
    faces = [
        [(0, 0), (face_size, 0), (face_size, face_size), (0, face_size)], # Центр
        [(0, face_size), (face_size, face_size), (face_size, face_size*2), (0, face_size*2)], # Низ 1
        [(0, face_size*2), (face_size, face_size*2), (face_size, face_size*3), (0, face_size*3)], # Низ 2
        [(0, -face_size), (face_size, -face_size), (face_size, 0), (0, 0)], # Верх
        [(-face_size, 0), (0, 0), (0, face_size), (-face_size, face_size)], # Лево
        [(face_size, 0), (face_size*2, 0), (face_size*2, face_size), (face_size, face_size)] # Право
    ]

    # 2. Функция рисования трапеции (улучшенная, учитывает направление вектора)
    def draw_tab(p1, p2):
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        length = math.hypot(dx, dy)
        if length == 0: return
        
        # Вектор нормали. Зависит от направления рисования (по часовой стрелке)
        nx = dy / length
        ny = -dx / length
        
        tab_depth = 6 
        inset = 5     
        
        t1 = (p1[0] + nx * tab_depth + dx/length * inset, p1[1] + ny * tab_depth + dy/length * inset)
        t2 = (p2[0] + nx * tab_depth - dx/length * inset, p2[1] + ny * tab_depth - dy/length * inset)
        
        pattern_group.add(dwg.polygon(points=[p1, t1, t2, p2], fill='#e0e0e0', stroke='black', stroke_width=0.5))
        pattern_group.add(dwg.line(start=p1, end=p2, stroke='black', stroke_dasharray="4,4"))

    # Сначала отрисовываем все грани куба
    for face in faces:
        pattern_group.add(dwg.polygon(points=face, fill='white', stroke='black', stroke_width=0.5))

    print("[+] Расчет топологических пар и генерация 7 клапанов...")
    
    # 3. Правильная расстановка 7 клапанов (по одному на каждое разрезанное ребро)
    
    # 3.1. Замыкание контура (Верх и Низ)
    # Выбираем только верхний клапан. Нижний край (Низ 2) остается без клапана.
    draw_tab((0, -face_size), (face_size, -face_size))     

    # 3.2. Боковые стыки верхней грани (стыкуются с верхушками Левой и Правой грани)
    draw_tab((0, 0), (0, -face_size))                      # Левый край Верхней грани
    draw_tab((face_size, -face_size), (face_size, 0))      # Правый край Верхней грани

    # 3.3. Боковые стыки грани Низ 1 (стыкуются с низом Левой и Правой грани)
    draw_tab((0, face_size*2), (0, face_size))             # Левый край Низ 1
    draw_tab((face_size, face_size), (face_size, face_size*2)) # Правый край Низ 1

    # 3.4. Боковые стыки грани Низ 2 (стыкуются с задней стенкой Левой и Правой грани)
    draw_tab((0, face_size*3), (0, face_size*2))           # Левый край Низ 2
    draw_tab((face_size, face_size*2), (face_size, face_size*3)) # Правый край Низ 2

    dwg.save()
    print(f"\n[!] Успех! Логически правильная выкройка сохранена в: {svg_filename}")

if __name__ == "__main__":
    main()
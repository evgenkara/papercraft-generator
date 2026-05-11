import svgwrite
import math

def generate_box_svg(w=40, d=60, h=30):
    # Создаем холст
    dwg = svgwrite.Drawing(size=('210mm', '297mm'), viewBox="-150 -150 300 350")
    pattern_group = dwg.add(dwg.g(id='papercraft-pattern', stroke='black', stroke_width=0.5, fill='none'))
    
    # 1. Параметрические координаты граней фургона
    faces = [
        [(0, 0), (w, 0), (w, d), (0, d)],                # Крыша (Центр)
        [(0, d), (w, d), (w, d+h), (0, d+h)],            # Лобовое стекло (Перед)
        [(0, d+h), (w, d+h), (w, d+h+d), (0, d+h+d)],    # Днище (Низ)
        [(0, -h), (w, -h), (w, 0), (0, 0)],              # Задняя дверь (Зад)
        [(-h, 0), (0, 0), (0, d), (-h, d)],              # Левый борт
        [(w, 0), (w+h, 0), (w+h, d), (w, d)]             # Правый борт
    ]

    # 2. Функция клапанов (с динамическим отступом)
    def draw_tab(p1, p2):
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        length = math.hypot(dx, dy)
        if length == 0: return
        nx, ny = dy / length, -dx / length
        tab_depth = 6
        # Защита: скос клапана не должен быть больше самой детали
        inset = min(5, length / 3)     
        
        t1 = (p1[0] + nx * tab_depth + dx/length * inset, p1[1] + ny * tab_depth + dy/length * inset)
        t2 = (p2[0] + nx * tab_depth - dx/length * inset, p2[1] + ny * tab_depth - dy/length * inset)
        
        pattern_group.add(dwg.polygon(points=[p1, t1, t2, p2], fill='#e0e0e0', stroke='black', stroke_width=0.5))
        pattern_group.add(dwg.line(start=p1, end=p2, stroke='black', stroke_dasharray="4,4"))

    # Отрисовка граней
    for face in faces:
        pattern_group.add(dwg.polygon(points=face, fill='white', stroke='black', stroke_width=0.5))

    # 3. Наши правильные 7 клапанов, адаптированные под новые координаты
    draw_tab((0, -h), (w, -h))               # Верх зада
    draw_tab((0, 0), (0, -h))                # Лево зада
    draw_tab((w, -h), (w, 0))                # Право зада
    draw_tab((0, d+h), (0, d))               # Лево переда
    draw_tab((w, d), (w, d+h))               # Право переда
    draw_tab((0, d+h+d), (0, d+h))           # Лево днища
    draw_tab((w, d+h), (w, d+h+d))           # Право днища

    return dwg.tostring()
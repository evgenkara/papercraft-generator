import svgwrite
import math

def generate_cube_svg():
    # Создаем SVG-объект в памяти (без привязки к реальному файлу)
    dwg = svgwrite.Drawing(size=('210mm', '297mm'), viewBox="-100 -150 300 350")
    pattern_group = dwg.add(dwg.g(id='papercraft-pattern', stroke='black', stroke_width=0.5, fill='none'))
    
    face_size = 40 
    
    faces = [
        [(0, 0), (face_size, 0), (face_size, face_size), (0, face_size)],
        [(0, face_size), (face_size, face_size), (face_size, face_size*2), (0, face_size*2)],
        [(0, face_size*2), (face_size, face_size*2), (face_size, face_size*3), (0, face_size*3)],
        [(0, -face_size), (face_size, -face_size), (face_size, 0), (0, 0)],
        [(-face_size, 0), (0, 0), (0, face_size), (-face_size, face_size)],
        [(face_size, 0), (face_size*2, 0), (face_size*2, face_size), (face_size, face_size)]
    ]

    def draw_tab(p1, p2):
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        length = math.hypot(dx, dy)
        if length == 0: return
        nx, ny = dy / length, -dx / length
        tab_depth, inset = 6, 5     
        
        t1 = (p1[0] + nx * tab_depth + dx/length * inset, p1[1] + ny * tab_depth + dy/length * inset)
        t2 = (p2[0] + nx * tab_depth - dx/length * inset, p2[1] + ny * tab_depth - dy/length * inset)
        
        pattern_group.add(dwg.polygon(points=[p1, t1, t2, p2], fill='#e0e0e0', stroke='black', stroke_width=0.5))
        pattern_group.add(dwg.line(start=p1, end=p2, stroke='black', stroke_dasharray="4,4"))

    for face in faces:
        pattern_group.add(dwg.polygon(points=face, fill='white', stroke='black', stroke_width=0.5))

    # Наши исправленные клапаны
    draw_tab((0, -face_size), (face_size, -face_size))     
    draw_tab((0, 0), (0, -face_size))                      
    draw_tab((face_size, -face_size), (face_size, 0))      
    draw_tab((0, face_size*2), (0, face_size))             
    draw_tab((face_size, face_size), (face_size, face_size*2)) 
    draw_tab((0, face_size*3), (0, face_size*2))           
    draw_tab((face_size, face_size*2), (face_size, face_size*3)) 

    # Возвращаем готовый SVG в виде строки, а не сохраняем в файл!
    return dwg.tostring()
from django.shortcuts import render
from .utils import generate_box_svg

def index(request):
    # Получаем параметры из URL (или ставим значения по умолчанию)
    w = int(request.GET.get('w', 40))
    d = int(request.GET.get('d', 60))
    h = int(request.GET.get('h', 30))
    
    # Генерируем SVG с новыми размерами
    svg_data = generate_box_svg(w=w, d=d, h=h)
    
    # Отправляем данные в шаблон HTML
    context = {
        'svg_data': svg_data,
        'w': w,
        'd': d,
        'h': h,
    }
    return render(request, 'generator/index.html', context)
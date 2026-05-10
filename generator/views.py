from django.http import HttpResponse
from .utils import generate_cube_svg

def index(request):
    svg_data = generate_cube_svg()
    
    # Временный простой HTML прямо во View (позже перенесем в templates)
    html = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <title>Papercraft MVP</title>
            <style>
                body {{ text-align: center; font-family: sans-serif; background-color: #f5f5f5; padding-top: 50px; }}
                .paper-sheet {{ 
                    background: white; width: 210mm; height: 297mm; 
                    margin: 0 auto; box-shadow: 0 4px 10px rgba(0,0,0,0.1); 
                    padding: 20px; box-sizing: border-box;
                }}
            </style>
        </head>
        <body>
            <h1>Генератор Papercraft (MVP)</h1>
            <p>Динамическая генерация 2D-выкройки на сервере</p>
            <div class="paper-sheet">
                {svg_data}
            </div>
        </body>
    </html>
    """
    return HttpResponse(html)
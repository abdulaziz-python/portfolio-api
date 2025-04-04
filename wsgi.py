import os
import sys
import json
from django.core.wsgi import get_wsgi_application
from django.urls import resolve
from django.http import HttpRequest, QueryDict
from io import BytesIO

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')

# Agar AlwaysData muhitida bo'lsa, bu o'zgaruvchini sozlaymiz
if os.environ.get('ALWAYSDATA_HTTPD_CONF'):
    os.environ['ALWAYSDATA'] = 'true'

application = get_wsgi_application()

# Netlify Functions orqali ishlaganda
if __name__ == "__main__" and len(sys.argv) > 3:
    method = sys.argv[1]
    path = sys.argv[2]
    request_data = json.loads(sys.argv[3])
    
    # HTTP so'rovni tayyorlash
    request = HttpRequest()
    request.method = method
    request.path = path
    request.path_info = path
    request.META['PATH_INFO'] = path
    
    # HTTP so'rovni serverda ishlayotgandek qilish
    request.META['SERVER_NAME'] = 'netlify.app'
    request.META['SERVER_PORT'] = '443'
    request.META['HTTP_HOST'] = 'api.abdulaziz.org.uz'
    request.META['REMOTE_ADDR'] = '127.0.0.1'
    
    # Headerlarni qo'shish
    for key, value in request_data.get('headers', {}).items():
        request.META[f'HTTP_{key.upper().replace("-", "_")}'] = value
    
    # Body va Query parametrlarini qo'shish
    if request.method in ['POST', 'PUT', 'PATCH']:
        request._body = request_data.get('body', '').encode('utf-8')
        
    query_params = QueryDict('', mutable=True)
    for key, value in request_data.get('queryParams', {}).items():
        query_params[key] = value
    request.GET = query_params
    
    # So'rovni bajarish
    match = resolve(path)
    response = match.func(request, *match.args, **match.kwargs)
    
    # Javobni tayyorlash
    status_code = response.status_code
    
    # Admin sahifalar uchun HTML, API uchun JSON javob
    is_admin = os.environ.get('ADMIN_REQUEST') == 'true'
    
    if hasattr(response, 'content'):
        content = response.content.decode('utf-8')
    else:
        content = ""
        
    # Status code va kontentni chiqarish
    print(status_code)
    print(content) 
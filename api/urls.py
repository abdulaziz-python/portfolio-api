from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
import requests
import json
from django.conf import settings
from django.shortcuts import render
from .views import PostViewSet, ProjectViewSet, SkillViewSet

router = DefaultRouter()
router.register('posts', PostViewSet)
router.register('projects', ProjectViewSet)
router.register('skills', SkillViewSet)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def generate_telegraph_token(request):
    short_name = request.data.get('short_name', 'Abdulaziz')
    author_name = request.data.get('author_name', 'Abdulaziz')
    
    url = "https://api.telegra.ph/createAccount"
    params = {
        "short_name": short_name,
        "author_name": author_name
    }
    
    try:
        r = requests.get(url, params=params)
        resp = r.json()
        
        if resp.get("ok"):
            return Response({
                'success': True,
                'access_token': resp["result"]["access_token"],
                'message': 'Token muvaffaqiyatli yaratildi'
            })
        else:
            return Response({
                'success': False,
                'error': resp.get('error'),
                'message': 'Telegraph API xatosi'
            })
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e),
            'message': 'So\'rov jo\'natishda xatolik'
        })

@api_view(['POST'])
@permission_classes([IsAdminUser])
def upload_image_to_telegraph(request):
    if 'image' not in request.FILES:
        return Response({
            'success': False, 
            'message': 'Rasm topilmadi'
        }, status=400)
    
    image = request.FILES['image']
    
    try:
        import base64
        url = 'https://telegra.ph/upload'
        
        # Faylni o'qish
        image_data = image.read()
        
        # Faylni ko'rsatishga tayyorlash
        files = {
            'file': ('image.jpg', image_data, 'image/jpeg')
        }
        
        r = requests.post(url, files=files)
        result = r.json()
        
        if isinstance(result, list) and len(result) > 0 and 'src' in result[0]:
            image_url = 'https://telegra.ph' + result[0]['src']
            return Response({
                'success': True,
                'url': image_url,
                'message': 'Rasm muvaffaqiyatli yuklandi'
            })
        else:
            return Response({
                'success': False,
                'error': result,
                'message': 'Telegraph API xatosi'
            }, status=400)
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e),
            'message': 'Rasmni yuklashda xatolik'
        }, status=500)

@api_view(['GET'])
def telegraph_page_info(request):
    path = request.query_params.get('path')
    
    if not path:
        return Response({
            'success': False,
            'message': 'Path parametri kerak'
        }, status=400)
    
    try:
        url = f'https://api.telegra.ph/getPage/{path}'
        params = {
            'return_content': True
        }
        
        r = requests.get(url, params=params)
        result = r.json()
        
        if result.get('ok'):
            return Response({
                'success': True,
                'result': result['result']
            })
        else:
            return Response({
                'success': False,
                'error': result.get('error'),
                'message': 'Telegraph API xatosi'
            }, status=400)
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e),
            'message': 'Ma\'lumot olishda xatolik'
        }, status=500)

def telegraph_pages_view(request):
    """Telegraph sahifalarini ko'rish sahifasi"""
    pages = []
    
    try:
        from django.conf import settings
        url = 'https://api.telegra.ph/getPageList'
        params = {
            'access_token': settings.TELEGRAPH_TOKEN,
            'limit': 50,
        }
        
        r = requests.get(url, params=params)
        result = r.json()
        
        if result.get('ok'):
            pages = result['result']['pages']
    except Exception as e:
        pages = []
    
    return render(request, 'admin/telegraph/pages.html', {
        'pages': pages,
        'title': 'Telegraph Pages',
    })

def telegraph_upload_view(request):
    """Telegraph sahifalariga rasm yuklash sahifasi"""
    return render(request, 'admin/telegraph/upload.html', {
        'title': 'Upload to Telegraph',
    })

urlpatterns = [
    path('', include(router.urls)),
    path('telegraph/token/', generate_telegraph_token, name='generate_telegraph_token'),
    path('telegraph/upload-image/', upload_image_to_telegraph, name='upload_image_to_telegraph'),
    path('telegraph/page-info/', telegraph_page_info, name='telegraph_page_info'),
    path('telegraph/pages/', telegraph_pages_view, name='telegraph-pages'),
    path('telegraph/upload/', telegraph_upload_view, name='telegraph-upload'),
] 
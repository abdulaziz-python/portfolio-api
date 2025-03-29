from celery import shared_task
from .models import Project
from django.utils import timezone
from django.core.files.storage import default_storage
import os

@shared_task
def cleanup_unused_images():
    all_projects = Project.objects.all()
    used_images = set(p.image.name for p in all_projects if p.image)
    
    image_dir = 'projects/'
    all_files = [f for f in default_storage.listdir(image_dir)[1] 
                if not f.endswith('.gitkeep')]
    
    all_image_paths = [os.path.join(image_dir, f) for f in all_files]
    
    count = 0
    for image_path in all_image_paths:
        if image_path not in used_images:
            default_storage.delete(image_path)
            count += 1
    
    return f"Deleted {count} unused project images" 
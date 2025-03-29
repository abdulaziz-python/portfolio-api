from celery import shared_task
from .models import Post
from django.utils import timezone

@shared_task
def cleanup_old_posts(days=365):
    cutoff_date = timezone.now() - timezone.timedelta(days=days)
    old_posts = Post.objects.filter(created_at__lte=cutoff_date)
    count = old_posts.count()
    old_posts.delete()
    return f"Deleted {count} posts older than {days} days" 
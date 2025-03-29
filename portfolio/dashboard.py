from django.db.models import Count
from blog.models import Post
from projects.models import Project, Skill
from django.utils import timezone
from datetime import timedelta

def dashboard_stats(request, context=None):
    # So'nggi 10 kunlik statistikani olish
    today = timezone.now().date()
    dates = [(today - timedelta(days=i)) for i in range(9, -1, -1)]
    date_labels = [d.strftime("%d/%m") for d in dates]
    
    # Har bir kategoriya uchun ma'lumotlar
    blog_stats = []
    project_stats = []
    skills_count = Skill.objects.count()
    
    # Har bir kun uchun statistikani hisoblaymiz
    for i, date in enumerate(dates):
        next_date = date + timedelta(days=1)
        
        # Blog postlar soni
        posts_count = Post.objects.filter(
            created_at__gte=date, 
            created_at__lt=next_date
        ).count()
        
        # Proyektlar soni
        projects_count = Project.objects.filter(
            created_at__gte=date, 
            created_at__lt=next_date
        ).count()
        
        # Random qiymatlar (demo uchun)
        visitors = 1000 + (i * 100) + (i % 3) * 200
        
        blog_stats.append(posts_count)
        project_stats.append(projects_count)
    
    # Dashboard statistikasi
    total_posts = Post.objects.count()
    total_projects = Project.objects.count()
    
    # Jadval ma'lumotlari
    category_stats = [
        {
            "title": "Group #1",
            "total": 36949,
            "data": [4576, 4617, 4401, 4308, 4040, 4688, 4741, 4629]
        },
        {
            "title": "Group #2",
            "total": 29722,
            "data": [4525, 3999, 4433, 3494, 3857, 2999, 3576, 2739]
        },
        {
            "title": "Group #3",
            "total": 22753,
            "data": [4132, 4237, 3542, 3230, 2561, 2038, 1340, 1673]
        },
        {
            "title": "Blog Posts",
            "total": total_posts,
            "data": [0, 0, 0, 0, 0, 0, 0, total_posts]
        },
        {
            "title": "Projects",
            "total": total_projects,
            "data": [0, 0, 0, 0, 0, 0, 0, total_projects]
        },
        {
            "title": "Skills",
            "total": skills_count,
            "data": [0, 0, 0, 0, 0, 0, 0, skills_count]
        }
    ]
    
    # Guruhlar uchun ranglar
    colors = ["bg-blue-500", "bg-sky-500", "bg-indigo-500", "bg-violet-500", "bg-purple-500", "bg-fuchsia-500"]
    
    # Progress ko'rsatkichlari
    progress_stats = [
        {"title": "Blog Posts", "value": total_posts, "percent": 5.58, "color": "text-green-500"},
        {"title": "Projects", "value": total_projects, "percent": 4.95, "color": "text-green-500"},
        {"title": "Skills", "value": skills_count, "percent": 4.68, "color": "text-green-500"}
    ]
    
    dashboard_context = {
        "title": "Dashboard",
        "widgets": [
            {
                "type": "stats_summary",
                "items": progress_stats
            },
            {
                "type": "chart",
                "title": "Statistics",
                "config": {
                    "type": "line",
                    "data": {
                        "labels": date_labels,
                        "datasets": [
                            {
                                "label": "Blog Posts",
                                "data": blog_stats,
                                "backgroundColor": "rgba(59, 130, 246, 0.5)",
                                "borderColor": "rgb(59, 130, 246)",
                            },
                            {
                                "label": "Projects",
                                "data": project_stats,
                                "backgroundColor": "rgba(16, 185, 129, 0.5)",
                                "borderColor": "rgb(16, 185, 129)",
                            }
                        ]
                    },
                    "options": {
                        "responsive": True,
                        "tension": 0.3
                    }
                }
            },
            {
                "type": "custom",
                "template": "admin/dashboard/stats_table.html",
                "context": {
                    "categories": category_stats,
                    "colors": colors,
                    "dates": ["March 20", "March 21", "March 22", "March 23", 
                              "March 24", "March 25", "March 26", "March 27"]
                }
            }
        ]
    }
    
    if context is not None:
        context.update(dashboard_context)
        return context
        
    return dashboard_context 
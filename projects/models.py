from django.db import models
from django.utils.text import slugify
import requests
import json

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon_url = models.URLField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    image_url = models.URLField(blank=True, null=True)
    description = models.TextField()
    telegraph_url = models.URLField(blank=True, null=True)
    telegraph_path = models.CharField(max_length=255, blank=True, null=True)
    telegraph_page_id = models.CharField(max_length=255, blank=True, null=True)
    skills = models.ManyToManyField(Skill, related_name='projects', blank=True)
    github_link = models.URLField(blank=True, null=True)
    live_link = models.URLField(blank=True, null=True)
    featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-featured', '-created_at']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            
        is_new = self.pk is None
        
        super().save(*args, **kwargs)
        
        if is_new or not self.telegraph_url:
            self.publish_to_telegraph()
        else:
            self.update_telegraph()
    
    def publish_to_telegraph(self):
        try:
            from django.conf import settings
            url = 'https://api.telegra.ph/createPage'
            
            content = self.prepare_content()
            
            data = {
                'access_token': settings.TELEGRAPH_TOKEN,
                'title': self.title,
                'content': json.dumps(content),
                'author_name': 'Abdulaziz',
                'return_content': True
            }
            
            r = requests.post(url, data=data)
            result = r.json()
            
            if result.get('ok'):
                self.telegraph_url = result['result']['url']
                self.telegraph_path = result['result']['path']
                if 'page_id' in result['result']:
                    self.telegraph_page_id = result['result']['page_id']
                
                models.Model.save(self, update_fields=['telegraph_url', 'telegraph_path', 'telegraph_page_id'])
        except Exception as e:
            print(f"Telegraph API error: {e}")
    
    def update_telegraph(self):
        try:
            if not self.telegraph_path:
                return self.publish_to_telegraph()
                
            from django.conf import settings
            url = 'https://api.telegra.ph/editPage'
            
            content = self.prepare_content()
            
            data = {
                'access_token': settings.TELEGRAPH_TOKEN,
                'path': self.telegraph_path,
                'title': self.title,
                'content': json.dumps(content),
                'author_name': 'Abdulaziz'
            }
            
            r = requests.post(url, data=data)
            result = r.json()
            
            if not result.get('ok'):
                print(f"Failed to update Telegraph: {result}")
                
        except Exception as e:
            print(f"Telegraph API error on update: {e}")
    
    def prepare_content(self):
        content = []
        
        if self.image_url:
            content.append({'tag': 'img', 'attrs': {'src': self.image_url}})
        
        paragraphs = self.description.split('\n\n')
        for p in paragraphs:
            if p.strip():
                content.append({'tag': 'p', 'children': [p.strip()]})
        
        skills = self.skills.all()
        if skills:
            skill_text = ", ".join([skill.name for skill in skills])
            content.append({'tag': 'p', 'children': [f"Skills: {skill_text}"]})
            
        links = []
        if self.github_link:
            links.append({'tag': 'a', 'attrs': {'href': self.github_link}, 'children': ['GitHub']})
        if self.live_link:
            links.append({'tag': 'a', 'attrs': {'href': self.live_link}, 'children': ['Live Demo']})
            
        if links:
            content.append({'tag': 'p', 'children': ['Links: '] + links})
        
        return content
    
    def fetch_from_telegraph(self):
        if not self.telegraph_path:
            return False
            
        try:
            url = f'https://api.telegra.ph/getPage/{self.telegraph_path}'
            params = {
                'return_content': True
            }
            
            r = requests.get(url, params=params)
            result = r.json()
            
            if result.get('ok'):
                page = result['result']
                content_list = page.get('content', [])
                
                description_parts = []
                for item in content_list:
                    if item.get('tag') == 'p' and item.get('children'):
                        # Skip skills and links paragraphs
                        text = ""
                        for child in item['children']:
                            if isinstance(child, str):
                                text += child
                        
                        if not text.startswith("Skills:") and not text.startswith("Links:"):
                            for child in item['children']:
                                if isinstance(child, str):
                                    description_parts.append(child)
                
                if description_parts:
                    self.description = '\n\n'.join(description_parts)
                    
                for item in content_list:
                    if item.get('tag') == 'img' and 'attrs' in item and 'src' in item['attrs']:
                        self.image_url = item['attrs']['src']
                        break
                        
                # Extract links
                for item in content_list:
                    if item.get('tag') == 'p' and item.get('children'):
                        text = ""
                        for child in item['children']:
                            if isinstance(child, str):
                                text += child
                                
                        if text.startswith("Links:"):
                            for child in item['children']:
                                if isinstance(child, dict) and child.get('tag') == 'a':
                                    link = child.get('attrs', {}).get('href', '')
                                    text = "".join(child.get('children', []))
                                    
                                    if text == "GitHub" and link:
                                        self.github_link = link
                                    elif text == "Live Demo" and link:
                                        self.live_link = link
                                    
                models.Model.save(self, update_fields=['description', 'image_url', 'github_link', 'live_link'])
                return True
                
        except Exception as e:
            print(f"Error fetching from Telegraph: {e}")
            
        return False
            
    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])

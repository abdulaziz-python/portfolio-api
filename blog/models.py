from django.db import models
from django.utils.text import slugify
from django.utils import timezone
import requests
import json
import base64
import re

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    image_url = models.URLField(blank=True, null=True)
    description = models.TextField()
    telegraph_url = models.URLField(blank=True, null=True)
    telegraph_path = models.CharField(max_length=255, blank=True, null=True)
    telegraph_page_id = models.CharField(max_length=255, blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
    
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
        from django.conf import settings
        token = settings.TELEGRAPH_TOKEN
        if not token:
            return False
        
        content = self.description
        
        content_html = self.convert_to_telegraph_format(content)
        
        url = "https://api.telegra.ph/createPage"
        data = {
            "access_token": token,
            "title": self.title,
            "content": json.dumps(content_html),
            "author_name": "Abdulaziz's Portfolio",
            "return_content": True
        }
        
        try:
            response = requests.post(url, data=data)
            result = response.json()
            
            if result.get("ok"):
                page = result.get("result")
                self.telegraph_url = page.get("url")
                self.telegraph_path = page.get("path")
                self.telegraph_page_id = page.get("page_id")
                self.save(update_fields=['telegraph_url', 'telegraph_path', 'telegraph_page_id'])
                return True
        except Exception as e:
            print(f"Telegraph error: {e}")
        
        return False
    
    def update_telegraph(self):
        from django.conf import settings
        token = settings.TELEGRAPH_TOKEN
        
        if not token or not self.telegraph_path:
            return False
        
        content = self.description
        content_html = self.convert_to_telegraph_format(content)
        
        url = "https://api.telegra.ph/editPage"
        data = {
            "access_token": token,
            "path": self.telegraph_path,
            "title": self.title,
            "content": json.dumps(content_html),
            "author_name": "Abdulaziz's Portfolio",
            "return_content": True
        }
        
        try:
            response = requests.post(url, data=data)
            result = response.json()
            
            if result.get("ok"):
                return True
        except Exception as e:
            print(f"Telegraph update error: {e}")
        
        return False
    
    def fetch_from_telegraph(self):
        from django.conf import settings
        token = settings.TELEGRAPH_TOKEN
        
        if not token or not self.telegraph_path:
            return False
        
        url = "https://api.telegra.ph/getPage"
        params = {
            "access_token": token,
            "path": self.telegraph_path,
            "return_content": True
        }
        
        try:
            response = requests.get(url, params=params)
            result = response.json()
            
            if result.get("ok"):
                page = result.get("result")
                content = page.get("content", [])
                
                markdown_text = self.convert_from_telegraph_format(content)
                self.description = markdown_text
                self.title = page.get("title", self.title)
                
                self.save(update_fields=['description', 'title'])
                return True
        except Exception as e:
            print(f"Telegraph fetch error: {e}")
        
        return False
    
    def convert_to_telegraph_format(self, text):
        md_blocks = text.split('\n\n')
        result = []
        
        for block in md_blocks:
            if block.strip():
                if block.startswith('# '):
                    result.append({"tag": "h3", "children": [block[2:]]})
                elif block.startswith('## '):
                    result.append({"tag": "h4", "children": [block[3:]]})
                elif block.startswith('![') and '](' in block and block.endswith(')'):
                    img_alt = block[2:block.index(']')]
                    img_url = block[block.index('(')+1:-1]
                    result.append({"tag": "img", "attrs": {"src": img_url, "alt": img_alt}})
                elif block.startswith('- '):
                    items = [line[2:] for line in block.split('\n') if line.startswith('- ')]
                    li_elements = [{"tag": "li", "children": [item]} for item in items]
                    result.append({"tag": "ul", "children": li_elements})
                elif re.match(r'^\d+\. ', block):
                    items = [line[line.index('.')+2:] for line in block.split('\n') if re.match(r'^\d+\. ', line)]
                    li_elements = [{"tag": "li", "children": [item]} for item in items]
                    result.append({"tag": "ol", "children": li_elements})
                else:
                    result.append({"tag": "p", "children": [block]})
        
        return result
    
    def convert_from_telegraph_format(self, content):
        markdown_lines = []
        
        for node in content:
            if isinstance(node, str):
                markdown_lines.append(node)
                continue
                
            tag = node.get("tag", "")
            children = node.get("children", [])
            attrs = node.get("attrs", {})
            
            if tag == "h3":
                text = children[0] if children and isinstance(children[0], str) else ""
                markdown_lines.append(f"# {text}\n")
            elif tag == "h4":
                text = children[0] if children and isinstance(children[0], str) else ""
                markdown_lines.append(f"## {text}\n")
            elif tag == "p":
                text = children[0] if children and isinstance(children[0], str) else ""
                markdown_lines.append(f"{text}\n")
            elif tag == "img":
                src = attrs.get("src", "")
                alt = attrs.get("alt", "")
                markdown_lines.append(f"![{alt}]({src})\n")
            elif tag == "ul":
                for li in children:
                    li_text = li.get("children", [""])[0] if isinstance(li.get("children", [""])[0], str) else ""
                    markdown_lines.append(f"- {li_text}")
                markdown_lines.append("\n")
            elif tag == "ol":
                for i, li in enumerate(children, 1):
                    li_text = li.get("children", [""])[0] if isinstance(li.get("children", [""])[0], str) else ""
                    markdown_lines.append(f"{i}. {li_text}")
                markdown_lines.append("\n")
                
        return "\n\n".join(markdown_lines)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.name} on {self.post.title}"

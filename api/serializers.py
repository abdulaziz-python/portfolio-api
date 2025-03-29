from rest_framework import serializers
from blog.models import Post
from projects.models import Project, Skill
import markdown

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']

class ProjectSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    
    class Meta:
        model = Project
        fields = ['id', 'title', 'slug', 'image', 'description', 'skills', 
                 'github_link', 'live_link', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    description_html = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'image', 'description', 
                 'description_html', 'created_at']
    
    def get_description_html(self, obj):
        return markdown.markdown(obj.description, extensions=['extra']) 
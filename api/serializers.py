from rest_framework import serializers
from blog.models import Post, Comment
from projects.models import Project, Skill
import markdown
from django.conf import settings

class SkillSerializer(serializers.ModelSerializer):
    project_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Skill
        fields = ['id', 'name', 'icon_url', 'project_count']
        
    def get_project_count(self, obj):
        return obj.projects.count()

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'name', 'email', 'text', 'created_at']
        extra_kwargs = {'email': {'write_only': True}}

class ProjectSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    absolute_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ['id', 'title', 'slug', 'image_url', 'description', 'skills', 
                 'github_link', 'live_link', 'telegraph_url', 'featured',
                 'views', 'created_at', 'absolute_url']
        
    def create(self, validated_data):
        instance = Project.objects.create(**validated_data)
        instance.fetch_from_telegraph()
        return instance
    
    def get_absolute_url(self, obj):
        return f"{settings.SITE_URL}/projects/{obj.slug}/"

class PostSerializer(serializers.ModelSerializer):
    description_html = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    absolute_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'image_url', 'description', 
                 'description_html', 'telegraph_url', 'views',
                 'created_at', 'comment_count', 'absolute_url']
                 
    def create(self, validated_data):
        instance = Post.objects.create(**validated_data)
        instance.fetch_from_telegraph()
        return instance
    
    def get_description_html(self, obj):
        return markdown.markdown(obj.description, extensions=['extra'])
    
    def get_comment_count(self, obj):
        return obj.comments.count()
        
    def get_absolute_url(self, obj):
        return f"{settings.SITE_URL}/blog/{obj.slug}/" 
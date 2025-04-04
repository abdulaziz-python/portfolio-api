from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django.db.models import F
from blog.models import Post, Comment
from projects.models import Project, Skill
from .serializers import PostSerializer, ProjectSerializer, SkillSerializer, CommentSerializer

# Create your views here.

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().select_related()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.query_params.get('latest'):
            return qs[:int(self.request.query_params.get('latest'))]
        return qs
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views = F('views') + 1
        instance.save(update_fields=['views'])
        
        # Sync with Telegraph if requested
        if request.query_params.get('sync') == 'true':
            instance.fetch_from_telegraph()
            
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_comment(self, request, slug=None):
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def comments(self, request, slug=None):
        post = self.get_object()
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def sync_from_telegraph(self, request, slug=None):
        post = self.get_object()
        success = post.fetch_from_telegraph()
        
        if success:
            return Response({
                "success": True,
                "message": "Successfully synced from Telegraph"
            })
        else:
            return Response({
                "success": False, 
                "message": "Failed to sync from Telegraph"
            }, status=status.HTTP_400_BAD_REQUEST)

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().prefetch_related('skills')
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        qs = super().get_queryset()
        skill = self.request.query_params.get('skill')
        featured = self.request.query_params.get('featured')
        
        if skill:
            qs = qs.filter(skills__name__icontains=skill)
        if featured == 'true':
            qs = qs.filter(featured=True)
            
        return qs.distinct()
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views = F('views') + 1
        instance.save(update_fields=['views'])
        
        # Sync with Telegraph if requested
        if request.query_params.get('sync') == 'true':
            instance.fetch_from_telegraph()
            
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def sync_from_telegraph(self, request, slug=None):
        project = self.get_object()
        success = project.fetch_from_telegraph()
        
        if success:
            return Response({
                "success": True,
                "message": "Successfully synced from Telegraph"
            })
        else:
            return Response({
                "success": False, 
                "message": "Failed to sync from Telegraph"
            }, status=status.HTTP_400_BAD_REQUEST)

class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    @action(detail=True, methods=['get'])
    def projects(self, request, pk=None):
        skill = self.get_object()
        projects = skill.projects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

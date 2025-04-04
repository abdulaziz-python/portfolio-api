from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Project, Skill
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from django.contrib.admin import SimpleListFilter

class StatusFilter(SimpleListFilter):
    title = 'status'
    parameter_name = 'status'
    
    def lookups(self, request, model_admin):
        return Project.STATUS_CHOICES
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status=self.value())
        return queryset

@admin.register(Skill)
class SkillAdmin(ModelAdmin):
    list_display = ('name', 'projects_count', 'show_icon')
    search_fields = ('name',)
    
    def projects_count(self, obj):
        count = obj.projects.count()
        return format_html('<span class="unfold-pill unfold-pill--primary">{}</span>', count)
    projects_count.short_description = "Proyektlar"
    
    def show_icon(self, obj):
        if obj.icon_url:
            return format_html('<img src="{}" alt="{}" width="24" height="24" />', obj.icon_url, obj.name)
        return ""
    show_icon.short_description = "Icon"

@admin.register(Project)
class ProjectAdmin(ModelAdmin):
    list_display = ('title', 'status_badge', 'show_image', 'created_at')
    list_filter = ('featured', StatusFilter, 'created_at', 'skills')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('skills',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'image_url', 'description', 'skills')
        }),
        ('Links', {
            'fields': ('demo_url', 'github_url', 'source_url'),
        }),
        ('Settings', {
            'fields': ('featured', 'status'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def status_badge(self, obj):
        colors = {
            'planning': 'warning',
            'in_progress': 'primary',
            'completed': 'success',
            'archived': 'default'
        }
        status_names = {
            'planning': 'Rejalashtirish',
            'in_progress': 'Ishlanmoqda',
            'completed': 'Bajarilgan',
            'archived': 'Arxivlangan'
        }
        
        return format_html('<span class="unfold-pill unfold-pill--{}">{}</span>', 
                          colors.get(obj.status, 'default'), 
                          status_names.get(obj.status, obj.status))
    status_badge.short_description = "Status"
    
    def show_image(self, obj):
        if obj.image_url:
            return format_html('<a href="{}" target="_blank"><img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" /></a>', obj.image_url, obj.image_url)
        return "-"
    show_image.short_description = "Rasm"

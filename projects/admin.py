from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Project, Skill

@admin.register(Skill)
class SkillAdmin(ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Project)
class ProjectAdmin(ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    list_filter = ('skills', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('skills',)
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'image', 'description', 'skills')
        }),
        ('Links', {
            'fields': ('github_link', 'live_link'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

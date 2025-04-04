from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Post, Comment
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline

class CommentInline(TabularInline):
    model = Comment
    extra = 0
    fields = ('name', 'email', 'text', 'created_at')
    readonly_fields = ('created_at',)
    can_delete = True

@admin.register(Post)
class PostAdmin(ModelAdmin):
    list_display = ('title', 'views_badge', 'telegraph_link', 'show_image', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('views', 'telegraph_url', 'telegraph_path', 'telegraph_page_id', 'created_at', 'updated_at', 'telegraph_preview')
    inlines = [CommentInline]
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'image_url', 'description')
        }),
        ('Telegraph', {
            'fields': ('telegraph_url', 'telegraph_path', 'telegraph_page_id', 'telegraph_preview'),
            'classes': ('collapse',),
        }),
        ('Stats', {
            'fields': ('views',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    actions = ['sync_from_telegraph']
    save_on_top = True
    
    def telegraph_preview(self, obj):
        if obj.telegraph_url:
            return format_html('<iframe src="{}" width="100%" height="500px"></iframe>', obj.telegraph_url)
        return "Telegraphda mavjud emas"
    telegraph_preview.short_description = "Telegraph Preview"
    
    def telegraph_link(self, obj):
        if obj.telegraph_url:
            return format_html('<a href="{}" target="_blank" class="button button-small"><i class="material-icons">launch</i></a>', obj.telegraph_url)
        return "-"
    telegraph_link.short_description = "Telegraph"
    
    def show_image(self, obj):
        if obj.image_url:
            return format_html('<a href="{}" target="_blank"><img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" /></a>', obj.image_url, obj.image_url)
        return "-"
    show_image.short_description = "Rasm"
    
    def views_badge(self, obj):
        color = "green"
        if obj.views > 50:
            color = "primary"
        if obj.views > 100:
            color = "purple"
            
        return format_html('<span class="unfold-pill unfold-pill--{}">{}</span>', color, obj.views)
    views_badge.short_description = "Ko'rishlar"
    
    def sync_from_telegraph(self, request, queryset):
        synced = 0
        for obj in queryset:
            if obj.fetch_from_telegraph():
                synced += 1
        
        self.message_user(request, f"{synced} ta post muvaffaqiyatli sinxronlashtirildi.")
    sync_from_telegraph.short_description = "Tanlangan postlarni Telegraphdan sinxronlash"

@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ('name', 'post_link', 'created_at')
    list_filter = ('created_at', 'post')
    search_fields = ('name', 'email', 'text')
    readonly_fields = ('created_at',)
    
    def post_link(self, obj):
        return format_html('<a href="{}">{}</a>', 
                          f'/admin/blog/post/{obj.post.id}/change/', 
                          obj.post.title)
    post_link.short_description = "Post"

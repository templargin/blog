from django.contrib import admin

from . models import Board, Topic, Post

# Register your models here.

class TopicInline(admin.TabularInline):
    model = Topic
    extra = 1

class BoardAdmin(admin.ModelAdmin):
    inlines = [TopicInline]
    list_display = ('name', 'description')

admin.site.register(Board, BoardAdmin)
admin.site.register(Topic)
admin.site.register(Post)

#admin.site.register(Board)

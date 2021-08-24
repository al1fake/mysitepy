from django.contrib import admin
from .models import Question, Comment
# Register your models here.
admin.site.register(Question)


class CommentAdmin(admin.ModelAdmin):
    #list_display = ('name', 'email', 'post', 'created', 'active')
    list_display = ('name', 'post', 'active')
    #list_filter = ('active', 'created', 'updated')
    list_filter = ('active',)
    #search_fields = ('name', 'email', 'body')
    search_fields = ('name', 'body')


admin.site.register(Comment, CommentAdmin)

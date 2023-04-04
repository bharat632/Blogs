from django.contrib import admin
from .models import Blog, Author, Tag, Comment
 
# Register your models here.


class BlogAdmin(admin.ModelAdmin):

    # readonly_fields = ('slug',)
    list_filter = ('title', )
    list_display = ('slug','date','author',)
    prepopulated_fields = {'slug':('title',)}

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('author_first_name','author_email',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user_email', 'blog']

admin.site.register(Blog,BlogAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Tag),
admin.site.register(Comment, CommentAdmin)

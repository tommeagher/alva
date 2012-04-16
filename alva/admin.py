from django.contrib import admin
from alva.models import Category, Idea

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}
    
class IdeaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}
    
admin.site.register(Idea, IdeaAdmin)
admin.site.register(Category, CategoryAdmin)
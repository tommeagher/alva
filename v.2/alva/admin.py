from django.contrib import admin
from alva.models import Category, Idea, UserProfile

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}
    
class IdeaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}
    
class UserProfileAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Idea, IdeaAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
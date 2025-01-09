from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import ServiceCategory, ServiceSubcategory, Service
from .models import Brochure, News

@admin.register(Brochure)
class BrochureAdmin(admin.ModelAdmin):
    list_display = ('title', 'file')
    search_fields = ('title',)
    
    fieldsets = (
        (None, {
            'fields': ('title', 'file')
        }),
    )

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'publication_date')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publication_date'
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'image')
        }),
        ('Contenido', {
            'fields': ('description',)
        }),
        ('Fecha', {
            'fields': ('publication_date',)
        }),
    )

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    """
    Configuración del admin para las categorías de servicios
    """
    list_display = ('name', 'description','order')
    search_fields = ('name', 'description')
    list_editable = ('order',)
    
    # Mostrar subcategorías inline
    class ServiceSubcategoryInline(admin.TabularInline):
        model = ServiceSubcategory
        extra = 1
        classes = ('collapse',)

    inlines = [ServiceSubcategoryInline]

@admin.register(ServiceSubcategory)
class ServiceSubcategoryAdmin(admin.ModelAdmin):
    """
    Configuración del admin para las subcategorías de servicios
    """
    list_display = ('name', 'category', 'order')
    search_fields = ('name', 'category__name')
    list_filter = ('category',)
    list_editable = ('order',)
    
    # Mostrar servicios inline
    class ServiceInline(admin.TabularInline):
        model = Service
        extra = 1
        classes = ('collapse',)

    inlines = [ServiceInline]

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """
    Configuración del admin para servicios individuales
    """
    list_display = ('title', 'subcategory', 'is_active', 'order')
    search_fields = ('title', 'description')
    list_filter = ('subcategory__category', 'subcategory', 'is_active')
    list_editable = ('is_active', 'order')

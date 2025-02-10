from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class Brochure(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name=_('Título del Brochure')
    )
    file = models.FileField(
        upload_to='brochures/',
        verbose_name=_('Archivo PDF'),
        help_text=_('Subir archivo en formato PDF')
    )

    class Meta:
        verbose_name = _('Brochure')
        verbose_name_plural = _('Brochures')
        ordering = ['title'] 
    def __str__(self):
        return self.title

class News(models.Model):
    title = models.CharField(
        max_length=255
    )
    slug = models.SlugField(
        max_length=255, 
        unique=True
    )
    description = models.TextField()
    image = models.ImageField(
        upload_to='news/', 
        null=True, 
        blank=True
    )
    publication_date = models.DateTimeField()

    class Meta:
        verbose_name = 'Noticia'
        verbose_name_plural = 'Noticias'
        ordering = ['-publication_date']

    def __str__(self):
        return self.title
    
class ServiceCategory(models.Model):
   
    name = models.CharField(
        max_length=255, 
        verbose_name=_('Nombre de Categoría')
    )
    image = models.ImageField(
        upload_to='service_categories/', 
        blank=True, 
        null=True, 
        verbose_name='Imagen 1'
    )
    order = models.PositiveIntegerField(
        default=0, 
        verbose_name=_('Orden de Presentación'),
        db_index=True
    )

    class Meta:
        verbose_name = _('Categoría de Servicio')
        verbose_name_plural = _('Categorías de Servicios')
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

class ServiceSubcategory(models.Model):
  
    category = models.ForeignKey(
        ServiceCategory, 
        on_delete=models.CASCADE, 
        related_name='subcategories',
        verbose_name=_('Categoría Principal')
    )
    name = models.CharField(
        max_length=255, 
        verbose_name=_('Nombre de Subcategoría')
    )
    description = models.TextField(
        blank=True, 
        null=True, 
        verbose_name=_('Descripción')
    )
    order = models.PositiveIntegerField(
        default=0, 
        verbose_name=_('Orden de Presentación'),
        db_index=True
    )

    class Meta:
        verbose_name = _('Subcategoría de Servicio')
        verbose_name_plural = _('Subcategorías de Servicios')
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.category.name} - {self.name}"

class Service(models.Model):
    subcategory = models.ForeignKey(
        ServiceSubcategory, 
        on_delete=models.SET_NULL,  
        related_name='services',
        verbose_name=_('Subcategoría'),
        null=True,  
        blank=True  
    )
    title = models.CharField(
        max_length=255, 
        verbose_name=_('Título del Servicio')
    )
    description = models.TextField(
        verbose_name=_('Descripción del Servicio')
    )
    image_1 = models.ImageField(
        upload_to='services/', 
        blank=True, 
        null=True, 
        verbose_name=_('Imagen 1')
    )
    image_2 = models.ImageField(
        upload_to='services/', 
        blank=True, 
        null=True, 
        verbose_name=_('Imagen 2')
    )
    order = models.PositiveIntegerField(
        default=0, 
        verbose_name=_('Orden de Presentación'),
        db_index=True
    )
    is_active = models.BooleanField(
        default=True, 
        verbose_name=_('Servicio Activo')
    )

    class Meta:
        verbose_name = _('Servicio')
        verbose_name_plural = _('Servicios')
        ordering = ['order', 'title']

    def __str__(self):
        return self.title
    
class Offer(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name=_('Título de la Oferta')
    )
    description = models.TextField(
        verbose_name=_('Descripción de la Oferta')
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Precio de la Oferta')
    )
    image = models.ImageField(
        upload_to='offers/',
        blank=True,
        null=True,
        verbose_name=_('Imagen de la Oferta')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Oferta Activa')
    )

    class Meta:
        verbose_name = _('Oferta')
        verbose_name_plural = _('Ofertas')
        ordering = ['title']

    def __str__(self):
        return self.title
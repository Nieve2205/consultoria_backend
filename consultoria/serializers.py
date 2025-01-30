# serializers.py
from rest_framework import serializers
from .models import ServiceCategory, ServiceSubcategory, Service
from .models import Brochure, News
from .models import Offer


class BrochureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brochure
        fields = ['id', 'title', 'file']
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        # Solo actualizar el archivo si se proporciona uno nuevo
        if 'file' not in validated_data:
            validated_data.pop('file', None)
        return super().update(instance, validated_data)

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'slug', 'description', 'image', 'publication_date']
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        # Manejar la actualización de la imagen solo si se proporciona una nueva
        if 'image' not in validated_data:
            validated_data.pop('image', None)
        return super().update(instance, validated_data)
    
class ServiceCategorySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, allow_empty_file=True, required=False)
    
    class Meta:
        model = ServiceCategory
        fields = ['id', 'name', 'description', 'image', 'order']

class ServiceSubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceSubcategory
        fields = ['id', 'category', 'name', 'description', 'order']

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'subcategory', 'title', 'description', 'image_1', 'image_2', 'order', 'is_active']

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ('id', 'title', 'description', 'services', 'price', 'image', 'is_active')
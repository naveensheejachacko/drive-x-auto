from django.contrib import admin
from .models import Vehicle, VehicleImage, Wishlist, Gallery

class VehicleImageInline(admin.TabularInline):
    model = VehicleImage
    extra = 1
    fields = ('image', 'is_primary')

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'price', 'fuel_type', 'body_type', 'created_by', 'created_at', 'is_active')
    list_filter = ('fuel_type', 'body_type', 'transmission', 'is_active', 'created_at')
    search_fields = ('title', 'description', 'color', 'engine')
    ordering = ('-created_at',)
    inlines = [VehicleImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'year', 'price', 'description')
        }),
        ('Technical Details', {
            'fields': ('fuel_type', 'transmission', 'engine', 'mileage', 'body_type', 'color')
        }),
        ('Features', {
            'fields': ('features',)
        }),
        ('Status', {
            'fields': ('is_active', 'created_by')
        }),
    )
    
    readonly_fields = ('created_by',)
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(VehicleImage)
class VehicleImageAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'is_primary', 'uploaded_at')
    list_filter = ('is_primary', 'uploaded_at')
    search_fields = ('vehicle__title',)
    ordering = ('-uploaded_at',)

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'vehicle', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('user__username', 'vehicle__title')
    ordering = ('-added_at',)

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_by', 'uploaded_at', 'is_active')
    list_filter = ('is_active', 'uploaded_at', 'uploaded_by')
    search_fields = ('title', 'description')
    ordering = ('-uploaded_at',)
    
    fieldsets = (
        ('Image Information', {
            'fields': ('title', 'description', 'image')
        }),
        ('Status', {
            'fields': ('is_active', 'uploaded_by')
        }),
    )
    
    readonly_fields = ('uploaded_by',)
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)

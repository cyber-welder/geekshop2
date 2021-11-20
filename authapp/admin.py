from django.contrib import admin

from authapp.models import ShopUser, ShopUserProfile


@admin.register(ShopUser)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_active')
    # fields = ()
    # readonly_fields = ()
    # ordering = ('-name',)
    search_fields = ('name',)


admin.site.register(ShopUserProfile)


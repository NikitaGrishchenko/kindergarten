from django.contrib import admin
from import_export import resources
from import_export.admin import ExportMixin

from .models import Day, Dish, Eating, Product, ProductInDish

# Register your models here.


# class ImportAdmin(admin.ModelAdmin):
#     change_list_template = 'templates/admin/change_list.html'

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "protein",
        "fats",
        "carbohydrates"
    )

admin.site.register(Product, ProductAdmin)


class ProductInDishInline(admin.TabularInline):
    model = ProductInDish
    # readonly_fields = ('protein', 'fats', 'carbohydrates')


class DishAdmin(admin.ModelAdmin):
    change_list_template = 'admin/change_list.html'

    inlines = [ProductInDishInline]
    list_display = (
        "name",
        "caloric"
    )

admin.site.register(Dish, DishAdmin)


class EatingInline(admin.TabularInline):
    model = Eating


class DayResource(resources.ModelResource):

    class Meta:
        model = Day
        import_id_fields = ("id",)
        fields = ('id', 'day_eating',)




class DayAdmin(ExportMixin, admin.ModelAdmin):
    inlines = [EatingInline]
    list_display = (
        "date",
        "type_group",
        "day_week",
        "parity_of_the_week",
    )
    resource_class = DayResource

admin.site.register(Day, DayAdmin)





from django import forms
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import NetworkLink, Product


@admin.register(NetworkLink)
class NetworkLinkAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "network_type",
        "level",
        "email",
        "country",
        "city",
        "street",
        "house_number",
        "debt_to_supplier",
        "supplier_link",
        "product_count",
        "view_products_link",
    )
    list_filter = ("city",)  # Фильтр по названию города
    actions = ["clear_debt"]  # Добавляем admin action для очистки задолженности

    def clear_debt(self, request, queryset):
        """Очищает задолженность перед поставщиком у выбранных объектов"""
        updated_count = queryset.update(debt_to_supplier=0.00)
        self.message_user(
            request, f"Задолженность успешно очищена для {updated_count} элементов."
        )

    clear_debt.short_description = "Очистить задолженность перед поставщиком"

    def product_count(self, obj):
        """Возвращает количество продуктов"""
        return obj.products.count()

    product_count.short_description = "Количество продуктов"

    def view_products_link(self, obj):
        """Возвращает ссылку на список продуктов звена сети"""
        url = reverse("admin:chain_product_changelist")
        return format_html(
            '<a href="{}?network_links__id__exact={}">Смотреть продукты</a>',
            url,
            obj.id,
        )

    view_products_link.short_description = "Продукты"

    def supplier_link(self, obj):
        """Возвращает ссылку на поставщика звена сети, если такой есть"""
        if obj.supplier:
            url = reverse("admin:chain_networklink_change", args=[obj.supplier.id])
            return format_html('<a href="{}">{}</a>', url, obj.supplier.name)
        return "Нет поставщика"

    supplier_link.short_description = "Поставщик"

    def get_fieldsets(self, request, obj=None):
        """Добавляет ссылку на поставщика на странице объекта сети"""
        fieldsets = super().get_fieldsets(request, obj)
        if obj and obj.supplier:
            supplier_url = reverse(
                "admin:chain_networklink_change", args=[obj.supplier.id]
            )
            supplier_link_html = format_html(
                '<a href="{}">{}</a>', supplier_url, obj.supplier.name
            )
            # Добавляем ссылку в заголовок первого fieldset'а или создаем новый
            if fieldsets:
                fieldsets[0] = (
                    fieldsets[0][0],
                    {
                        **fieldsets[0][1],
                        "description": f"Ссылка на поставщика: {supplier_link_html}",
                    },
                )
        return fieldsets


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "model",
            "release_date",
            "network_links",
        ]  # Добавляем поле для связей


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ("name", "model", "release_date", "get_network_links")
    list_filter = ("name", "release_date")
    search_fields = (
        "name",
        "model",
    )

    def get_network_links(self, obj):
        return ", ".join(
            [link.name for link in obj.network_links.all()]
        )  # Выводим связанные с продуктом звенья сети

    get_network_links.short_description = "Звенья сети"

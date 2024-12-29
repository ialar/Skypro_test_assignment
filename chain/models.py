from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import models

NULLABLE = {"null": True, "blank": True}


class NetworkLink(models.Model):
    TYPE_CHOICES = [
        ("factory", "Завод"),
        ("retail", "Розничная сеть"),
        ("individual", "Индивидуальный предприниматель"),
    ]

    # Название звена сети
    name = models.CharField(max_length=255, verbose_name="Название")

    # Тип звена сети
    network_type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default="retail",
        verbose_name="Тип звена сети",
    )

    # Контакты
    email = models.EmailField(unique=True, verbose_name="Почта")
    country = models.CharField(max_length=100, verbose_name="Страна")
    city = models.CharField(max_length=100, verbose_name="Город")
    street = models.CharField(max_length=255, verbose_name="Улица")
    house_number = models.CharField(max_length=10, verbose_name="Номер дома")

    # Поставщик (самоссылка)
    supplier = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        related_name="clients",
        verbose_name="Поставщик",
        **NULLABLE,
    )

    # Задолженность перед поставщиком
    debt_to_supplier = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, verbose_name="Задолженность"
    )

    # Время создания
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"{self.name} (уровень - {self.level}) - создан {self.created_at}"

    @property
    @admin.display(description="Уровень иерархии")
    def level(self):
        """
        Рассчитывает уровень объекта в иерархии:
        - Завод (уровень 0) - фиксированный уровень.
        - Розница и ИП могут иметь разные уровни
        в зависимости от возможных взаимных поставок.
        """
        current_level = 0
        current_supplier = self.supplier
        current_object = self  # Сохраняем ссылку на текущее звено сети

        # Рекурсивно проверяем наличие поставщиков у звена
        while current_supplier:
            # В данной версии приложения реализован запрет на самопоставку через метод clean.
            # Но данная проверка все равно может быть полезна в некоторых ситуациях.
            # Например, временное изменение бизнес-логики и отмена валидации на самопоставку.
            if current_supplier == current_object:
                break  # Исключаем запуск бесконечного цикла при самопоставке
            current_level += 1
            current_supplier = current_supplier.supplier
        return current_level

    def clean(self):
        super().clean()
        # Проверка на отрицательную задолженность
        if self.debt_to_supplier < 0:
            raise ValidationError(
                {"debt_to_supplier": "Задолженность не может быть отрицательной."}
            )
        # Проверка на самопоставку
        if self.supplier == self:
            raise ValidationError("Нельзя выбрать себя в качестве поставщика.")

    class Meta:
        verbose_name = "Звено сети"
        verbose_name_plural = "Звенья сети"


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название продукта")
    model = models.CharField(max_length=255, verbose_name="Модель продукта")
    release_date = models.DateField(verbose_name="Дата выхода")
    network_links = models.ManyToManyField(
        NetworkLink,
        related_name="products",
        verbose_name="Звенья сети",
    )

    def __str__(self):
        return f"{self.name} ({self.model}) - на рынке с {self.release_date}"

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

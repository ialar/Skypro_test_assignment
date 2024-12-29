from rest_framework.serializers import ModelSerializer

from chain.models import NetworkLink, Product
from chain.validators import validate_debt_update


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "model", "release_date", "network_links"]


class NetworkLinkSerializer(ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = NetworkLink
        fields = [
            "id",
            "name",
            "network_type",
            "level",
            "email",
            "country",
            "city",
            "street",
            "house_number",
            "supplier",
            "debt_to_supplier",
            "created_at",
            "products",
        ]
        # Если не хотим явно сообщать о запрете обновления, можно определить поле только на чтение
        # read_only_fields = ["debt_to_supplier"]

    def validate(self, attrs):
        # Проверяем обновление поля задолженности
        validate_debt_update(attrs)
        return attrs

    def update(self, instance, validated_data):
        # Обновляем остальные поля и сохраняем изменения
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

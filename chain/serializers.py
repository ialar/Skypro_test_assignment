from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from chain.models import NetworkLink, Product, Address
from chain.validators import validate_debt_update


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = ['country', 'city', 'street', 'house_number']


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "model", "release_date", "network_links"]


class NetworkLinkSerializer(ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    address = AddressSerializer()

    class Meta:
        model = NetworkLink
        fields = [
            "id",
            "name",
            "network_type",
            "level",
            "email",
            "address",
            "supplier",
            "debt_to_supplier",
            "created_at",
            "products",
        ]
        read_only_fields = ["products"]

    def create(self, validated_data):
        address_data = validated_data.pop("address")
        address = Address.objects.create(**address_data)
        products_data = validated_data.pop("products", [])

        instance = NetworkLink.objects.create(address=address, **validated_data)
        instance.products.set(products_data)
        return instance

    def update(self, instance, validated_data):
        address_data = validated_data.pop("address")
        address = instance.address
        address.country = address_data.get("country", address.country)
        address.city = address_data.get("city", address.city)
        address.street = address_data.get("street", address.street)
        address.house_number = address_data.get("house_number", address.house_number)
        address.save()

        products_data = validated_data.pop("products", None)
        if products_data is not None:
            if not products_data:
                raise ValidationError({"products": "This field cannot be empty"})
            instance.products.clear()
            instance.products.add(*products_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

    def validate(self, attrs):
        # Проверяем обновление поля задолженности
        validate_debt_update(attrs)
        return attrs

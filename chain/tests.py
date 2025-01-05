from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from chain.models import Address, NetworkLink, Product
from users.models import User


class NetworkLinkTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@test.com", is_active=True)
        self.client.force_authenticate(user=self.user)
        self.address = Address.objects.create(
            country="Test Country",
            city="Test City",
            street="Test Street",
            house_number="1A",
        )
        self.product = Product.objects.create(
            name="Test Product",
            model="Test Model",
            release_date="2020-10-01",
        )
        self.network_link = NetworkLink.objects.create(
            name="Test Link",
            email="test@example.com",
            address=self.address,
            debt_to_supplier=0.00,
        )
        self.network_link.products.add(self.product)
        self.url = reverse("chain:network_link-list")
        self.detail_url = reverse(
            "chain:network_link-detail", args=[self.network_link.id]
        )

    def test_create_network_link_instance(self):
        """Тестируем создание экземпляра звена сети."""
        self.assertEqual(self.network_link.name, "Test Link")
        self.assertEqual(self.network_link.email, "test@example.com")
        self.assertEqual(self.network_link.address.country, "Test Country")
        self.assertEqual(self.network_link.address.city, "Test City")
        self.assertEqual(self.network_link.address.street, "Test Street")
        self.assertEqual(self.network_link.address.house_number, "1A")
        self.assertEqual(self.network_link.debt_to_supplier, 0.00)

    def test_negative_debt_validation(self):
        """Тестируем валидацию отрицательной задолженности."""
        self.network_link.debt_to_supplier = -100.00
        with self.assertRaises(ValidationError) as context:
            self.network_link.clean()
        self.assertIn(
            "Задолженность не может быть отрицательной.", str(context.exception)
        )

    def test_self_supplier_validation(self):
        """Тестируем валидацию самопоставки."""
        self.network_link.supplier = self.network_link
        with self.assertRaises(ValidationError) as context:
            self.network_link.clean()
        self.assertIn(
            "Нельзя выбрать себя в качестве поставщика.", context.exception.messages
        )

    def test_create_network_link_with_debt_to_supplier(self):
        """Тестируем создание нового звена сети с задолженностью перед поставщиком."""
        data = {
            "name": "New Link",
            "email": "new@example.com",
            "address": {
                "country": "New Country",
                "city": "New City",
                "street": "New Street",
                "house_number": "2B",
            },
            "debt_to_supplier": 100.00,
        }
        response = self.client.post(self.url, data, format="json")

        # Проверяем, что запрос завершился с ошибкой валидации
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)
        self.assertEqual(
            response.data["non_field_errors"][0],
            "Обновление задолженности перед поставщиком запрещено через API.",
        )

    def test_create_network_link_without_debt_to_supplier(self):
        """Тестируем создание нового звена сети без задолженности перед поставщиком."""
        data = {
            "name": "New Link",
            "email": "new@example.com",
            "address": {
                "country": "New Country",
                "city": "New City",
                "street": "New Street",
                "house_number": "2B",
            },
        }
        response = self.client.post(self.url, data, format="json")
        # print(response.content)

        # Проверяем, что объект создан успешно
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(NetworkLink.objects.count(), 2)
        self.assertEqual(NetworkLink.objects.last().name, "New Link")

    def test_retrieve_network_link(self):
        """Тестируем получение существующего звена сети."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.network_link.name)

    def test_update_network_link(self):
        """Тестируем обновление существующего звена сети."""
        address_data = {
            "country": "Updated Country",
            "city": "Updated City",
            "street": "Updated Street",
            "house_number": "1B",
        }
        data = {
            "name": "Updated Link",
            "email": "updated@example.com",
            "address": address_data,
        }
        response = self.client.put(self.detail_url, data, format="json")

        # Проверяем, что запрос обновления прошел успешно
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.network_link.refresh_from_db()  # Обновляем объект из базы данных
        self.assertEqual(self.network_link.name, "Updated Link")
        self.assertEqual(self.network_link.email, "updated@example.com")
        self.assertEqual(self.network_link.address.country, "Updated Country")
        self.assertEqual(self.network_link.address.city, "Updated City")
        self.assertEqual(self.network_link.address.street, "Updated Street")
        self.assertEqual(self.network_link.address.house_number, "1B")

    def test_update_debt_to_supplier_field(self):
        """Тестируем обновление поля задолженности."""
        data = {"debt_to_supplier": 1.00}
        response = self.client.patch(self.detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)
        self.assertEqual(
            response.data["non_field_errors"][0],
            "Обновление задолженности перед поставщиком запрещено через API.",
        )

    def test_delete_network_link(self):
        """Тестируем удаление существующего звена сети."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            NetworkLink.objects.count(), 0
        )  # Проверяем, что объект был удален

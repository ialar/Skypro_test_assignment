from rest_framework.exceptions import ValidationError


def validate_debt_update(attrs):
    if "debt_to_supplier" in attrs:
        raise ValidationError(
            "Обновление задолженности перед поставщиком запрещено через API."
        )

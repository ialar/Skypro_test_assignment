from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from chain.models import NetworkLink
from chain.serializers import NetworkLinkSerializer
from users.permissions import IsActiveEmployee


class NetworkLinkViewSet(ModelViewSet):
    queryset = NetworkLink.objects.all()
    serializer_class = NetworkLinkSerializer
    permission_classes = [IsActiveEmployee]

    def get_queryset(self):
        """Добавлена возможность фильтрации объектов по определенной стране
        (если передан параметр `country`).
        """
        queryset = super().get_queryset()
        country = self.request.query_params.get("country")
        if country:
            queryset = queryset.filter(country=country)
        return queryset

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

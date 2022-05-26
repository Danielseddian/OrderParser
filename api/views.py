from rest_framework.viewsets import ReadOnlyModelViewSet

from .serializers import Order, OrderSerializer


class OrderViewSet(ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

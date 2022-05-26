from rest_framework import serializers

from .models import Order
from .tools import get_exchange


class OrderSerializer(serializers.ModelSerializer):
    price_rouble = serializers.SerializerMethodField()

    class Meta:
        fields = ("own_id", "order_id", "price", "delivery_date", "price_rouble")
        model = Order

    def get_price_rouble(self):
        return format(self.data["price"] * get_exchange(), ".2f")

from rest_framework import serializers

from .models import Order
from .tools import get_exchange


class OrderSerializer(serializers.ModelSerializer):
    price_rouble = serializers.SerializerMethodField()

    class Meta:
        fields = ("own_id", "order_id", "price", "price_rouble", "delivery_date")
        model = Order

    def get_price_rouble(self, obj):
        return format(obj.price * get_exchange(), ".2f")

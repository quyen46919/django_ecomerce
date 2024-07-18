from rest_framework import serializers
from .models import Order, OrderDetail, OrderStatus
from products.serializers import ProductSerializer
from user.serializers import MyTokenObtainPairSerializer


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = '__all__'


class OrderStatusSerializer(serializers.ModelSerializer):
    product = ProductSerializer(source='product_id')
    user = MyTokenObtainPairSerializer(source='user_id')
    order = OrderSerializer(source='order_id')
    o_detail = OrderDetailSerializer(source='o_detail_id')

    class Meta:
        model = OrderStatus
        fields = ['id', 'status', 'reason', 'created_at', 'updated_at', 'deleted_at', 'product', 'user', 'order', 'o_detail']  

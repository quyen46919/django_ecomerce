from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from products.models import Product
from .shared.enum.order_status import OrderStatusEnum


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    receiver_name = models.CharField(max_length=255)
    receiver_phone = models.CharField(max_length=15)
    receiver_address = models.CharField(max_length=255)
    is_ordered = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    total = models.FloatField(default=0)
    description = models.CharField(max_length=512)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    payment_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['created_at'])
        ]

    # Kiểm tra xem những sản phẩm trong đơn hàng có còn đủ hàng hay không
    def checkValidOrder(self):
        products = [] # List sản phẩm không hợp lệ
        flag = True # Cờ để check có lỗi hay không, mặc định là True -> Không có sản phẩm lỗi

        # sử dụng self.<foreign_table_related_name>.all() để lấy ra toàn bộ những record của bảng ngoại
        for order_detail in self.order_details.all():
            try:
                # với mỗi record, check xem amount trong đơn hàng có lớn hơn bằng số lượng đặt hàng hay không
                product = Product.objects.get(id=order_detail.product_id.id)
                if order_detail.amount > product.amount:
                    # đổi flag sang False -> đơn hàng ko hợp lệ
                    if flag:
                        flag = False
                    # Lưu thông tin sản phẩm bị lỗi để gửi về cho FE
                    products.append({
                        'product_id': product.id,
                        'product_name': product.name,
                        'product_amount': product.amount,
                        'order_amount': order_detail.amount,
                        'reason': 'Not enough stocks to supply'
                    })
            # Sản phẩm không tìm thấy, đổi flag và trả về thông tin sản phẩm bị lỗi
            except Product.DoesNotExist:
                if flag:
                    flag = False
                products.append({
                    'product_id': order_detail.product_id.id,
                    'reason': 'Product has been removed or is out of stock'
                })
        return {'status': flag, 'data': products}


class OrderDetail(models.Model):
    id = models.AutoField(primary_key=True)
    amount = models.IntegerField()
    price = models.FloatField()
    discount = models.IntegerField(default=0)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_details', null=False)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)


class OrderStatus(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20, choices=OrderStatusEnum.choices)
    reason = models.CharField(max_length=255)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, null=False)
    o_detail_id = models.ForeignKey(OrderDetail, on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)



@receiver([post_save, post_delete], sender=OrderDetail)
def update_order_total(sender, instance, **kwargs):
    order = instance.order_id
    total = sum((detail.price - (detail.price * detail.discount / 100)) * detail.amount
                for detail in order.order_details.all())
    order.total = total
    order.save()


# Khi thanh toán đơn hàng thành công, cần update lại số lượng sản phẩm trong product
@receiver(post_save, sender=Order)
def update_product_amount(sender, instance, **kwargs):
    if instance.is_paid:
        order_details = OrderDetail.objects.filter(order_id=instance.id)
        for detail in order_details:
            product = Product.objects.get(id=detail.product_id.id)
            product.amount -= detail.amount
            product.save()

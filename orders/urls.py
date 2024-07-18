from django.urls import path
from orders import views

urlpatterns = [
    path("orders/", views.OrderAPIView.as_view()),
    path("orders/<slug:id_slug>/", views.OrderDetailAPIView.as_view()),
    path("orders/<slug:order_id_slug>/detail/", views.OrderDetailWithProductAPIView.as_view()),
    path("orders/<slug:order_id_slug>/detail/<slug:id_slug>/", views.OrderDetailWithProductDetailAPIView.as_view()),

    # order status
    path("order_status/", views.OrderStatusAPIView.as_view()),
    path("order_status/<slug:id_slug>/", views.OrderStatusDetailAPIView.as_view()),
    # order cancel status
    path("order_cancel/", views.OrderCancelStatusAPIView.as_view()),
    # Paypal payment
    path("orders/<slug:order_id_slug>/payment/", views.OrderCheckoutAPIView.as_view()),
    path("orders/<slug:order_id_slug>/payment/verify/", views.VerifyPaymentAPIView.as_view())
]

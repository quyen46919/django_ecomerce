from django.urls import path
from products import views

urlpatterns = [
    path("category/", views.CategoryAPIView.as_view()),
    path("category/<slug:id_slug>/", views.CategoryDetailAPIView.as_view()),
    
    path("product/<slug:product_id_slug>/images/", views.ProductImageAPIView.as_view()),
    path("product/<slug:product_id_slug>/images/<slug:id_slug>/", views.ProductImageDetailAPIView.as_view()),
    
    path("product/<slug:product_id_slug>/comments/", views.ProductCommentAPIView.as_view()),
    path("product/<slug:product_id_slug>/comments/<slug:id_slug>/", views.ProductCommentDetailAPIView.as_view()),
    
    path("product/", views.ProductViewAPI.as_view()),
    path("product/<slug:id_slug>/", views.ProductDetailAPIView.as_view()),
    path("filter/", views.ProductFilterViewAPI.as_view()),
]

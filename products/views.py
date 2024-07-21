from rest_framework import views
from rest_framework.permissions import AllowAny
from django.http import Http404
from django.contrib.auth import get_user_model
from backend_ecommerce.helpers import custom_response, parse_request
from .models import Category, Product, ProductImage, ProductComment
from .serializers import CategorySerializer, ProductSerializer, ProductImageSerializer, ProductCommentSerializer
from filter_and_pagination import FilterPagination
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
User = get_user_model()


class CategoryAPIView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            queryset = FilterPagination.filter_and_pagination(request, Category)
            serialize_data = CategorySerializer(queryset['queryset'], many=True).data
            result_set = {'list': serialize_data, 'pagination': queryset['pagination']}
            return custom_response('Get all categories successfully!', 'Success', result_set, 200)
        except:
            return custom_response('Get all categories failed!', 'Error', None, 400)

    def post(self, request):
        data = parse_request(request)
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return custom_response('Create category successfully!', 'Success', serializer.data, 201)
        else:
            return custom_response('Create category failed', 'Error', serializer.errors, 400)


class CategoryDetailAPIView(views.APIView):
    permission_classes = [AllowAny]

    def get_object(self, id_slug):
        try:
            return Category.objects.get(id=id_slug)
        except:
            raise Http404

    def get(self, request, id_slug, format=None):
        try:
            category = self.get_object(id_slug)
            serializer = CategorySerializer(category)
            return custom_response('Get category successfully!', 'Success', serializer.data, 200)
        except:
            return custom_response('Get category failed!', 'Error', "Category not found!", 400)

    def put(self, request, id_slug):
        try:
            data = parse_request(request)
            category = self.get_object(id_slug)
            serializer = CategorySerializer(category, data=data)
            if serializer.is_valid():
                serializer.save()
                return custom_response('Update category successfully!', 'Success', serializer.data, 200)
            else:
                return custom_response('Update category failed', 'Error', serializer.errors, 400)
        except:
            return custom_response('Update category failed', 'Error', "Category not found!", 400)

    def delete(self, request, id_slug):
        try:
            category = self.get_object(id_slug)
            category.delete()
            return custom_response('Delete category successfully!', 'Success', {"category_id": id_slug}, 204)
        except:
            return custom_response('Delete category failed!', 'Error', "Category not found!", 400)


class ProductViewAPI(views.APIView):
    permission_classes = [AllowAny] 

    def get(self, request):
        try:
            queryset = FilterPagination.filter_and_pagination(request, Product)
            serialize_data = ProductSerializer(queryset['queryset'], many=True).data
            result_set = {'list': serialize_data, 'pagination': queryset['pagination']}
            return custom_response('Get all products successfully!', 'Success', result_set, 200)
        except:
            return custom_response('Get all products failed!', 'Error', None, 400)

    def post(self, request):
        try:
            data = parse_request(request)
            category = Category.objects.get(id=data['category_id'])
            product = Product(
                name=data['name'],
                unit=data['unit'],
                price=data['price'],
                discount=data['discount'],
                amount=data['amount'],
                thumbnail=data['thumbnail'],
                category_id=category
            )
            product.save()
            serializer = ProductSerializer(product)
            return custom_response('Create product successfully!', 'Success', serializer.data, 201)
        except Exception as e:
            return custom_response('Create product failed', 'Error', [str(e)], 400)


class ProductDetailAPIView(views.APIView):
    permission_classes = [AllowAny]

    def get_object(self, id_slug):
        try:
            return Product.objects.get(id=id_slug)
        except:
            raise Http404

    def get(self, request, id_slug, format=None):
        try:
            product = self.get_object(id_slug)
            serializer = ProductSerializer(product)
            return custom_response('Get product successfully!', 'Success', serializer.data, 200)
        except:
            return custom_response('Get product failed!', 'Error', "Product not found!", 400)

    def put(self, request, id_slug):
        try:
            data = parse_request(request)
            product = self.get_object(id_slug)
            serializer = ProductSerializer(product, data=data)
            if serializer.is_valid():
                serializer.save()
                return custom_response('Update product successfully!', 'Success', serializer.data, 200)
            else:
                return custom_response('Update product failed', 'Error', serializer.errors, 400)
        except:
            return custom_response('Update product failed', 'Error', "Category not found!", 400)

    def delete(self, request, id_slug):
        try:
            product = self.get_object(id_slug)
            product.delete()
            return custom_response('Delete product successfully!', 'Success', {"product_id": id_slug}, 204)
        except:
            return custom_response('Delete product failed!', 'Error', "Product not found!", 400)


class ProductImageAPIView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request, product_id_slug):
        try:
            product_images = ProductImage.objects.filter(product_id=product_id_slug).all()
            serializers = ProductImageSerializer(product_images, many=True)
            return custom_response('Get all product images successfully!', 'Success', serializers.data, 200)
        except:
            return custom_response('Get all product images failed!', 'Error', 'Product images not found', 400)

    def post(self, request, product_id_slug):
        try:
            data = parse_request(request)
            product = Product.objects.get(id=data['product_id'])
            product_image = ProductImage(
                product_id=product,
                image_url=data['image_url']
            )
            product_image.save()
            serializer = ProductImageSerializer(product_image)
            return custom_response('Create product image successfully!', 'Success', serializer.data, 201)
        except Exception as e:
            return custom_response('Create product image failed', 'Error', [str(e)], 400)


class ProductImageDetailAPIView(views.APIView):
    permission_classes = [AllowAny]

    def get_object(self, id_slug):
        try:
            return ProductImage.objects.get(id=id_slug)
        except:
            raise Http404

    def get_object_with_product_id(self, product_id_slug, id_slug):
        try:
            return ProductImage.objects.get(product_id=product_id_slug, id=id_slug)
        except:
            raise Http404

    def get(self, request, product_id_slug, id_slug, format=None):
        try:
            product_image = self.get_object(id_slug)
            serializer = ProductImageSerializer(product_image)
            return custom_response('Get product image successfully!', 'Success', serializer.data, 200)
        except:
            return custom_response('Get product image failed!', 'Error', "Product image not found!", 400)

    def put(self, request, product_id_slug, id_slug):
        try:
            data = parse_request(request)
            product_image = self.get_object_with_product_id(product_id_slug, id_slug)
            serializer = ProductImageSerializer(product_image, data=data)
            if serializer.is_valid():
                serializer.save()
                return custom_response('Update product image successfully!', 'Success', serializer.data, 200)
            else:
                return custom_response('Update product image failed', 'Error', serializer.errors, 400)
        except:
            return custom_response('Update product image failed', 'Error', "Product image not found!", 400)

    def delete(self, request, product_id_slug, id_slug):
        try:
            product_image = self.get_object_with_product_id(product_id_slug, id_slug)
            product_image.delete()
            return custom_response('Delete product image successfully!', 'Success', {"product_image_id": id_slug}, 204)
        except:
            return custom_response('Delete product image failed!', 'Error', "Product image not found!", 400)


class ProductCommentAPIView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request, product_id_slug):
        try:
            product_comments = ProductComment.objects.filter(product_id=product_id_slug).all()
            serializers = ProductCommentSerializer(product_comments, many=True)
            return custom_response('Get all product comments successfully!', 'Success', serializers.data, 200)
        except:
            return custom_response('Get all product comments failed!', 'Error', None, 400)

    def post(self, request, product_id_slug):
        try:
            data = parse_request(request)
            product = Product.objects.get(id=data['product_id'])
            parent_comment_id = ProductComment.objects.get(id=data['parent_id'])
            user = User.objects.get(id=data['user_id'])
            product_comment = ProductComment(
                product_id=product,
                rating=data['rating'],
                comment=data['comment'],
                user_id=user,
                parent_id=parent_comment_id
            )
            product_comment.save()
            serializer = ProductCommentSerializer(product_comment)
            return custom_response('Create product comment successfully!', 'Success', serializer.data, 201)
        except Exception as e:
            return custom_response('Create product comment failed', 'Error', [str(e)], 400)


class ProductCommentDetailAPIView(views.APIView):
    permission_classes = [AllowAny]

    def get_object(self, id_slug):
        try:
            return ProductComment.objects.get(id=id_slug)
        except:
            raise Http404

    def get_object_with_product_id(self, product_id_slug, id_slug):
        try:
            return ProductComment.objects.get(product_id=product_id_slug, id=id_slug)
        except:
            raise Http404

    def get(self, request, product_id_slug, id_slug, format=None):
        try:
            product_comment = self.get_object(id_slug)
            serializer = ProductCommentSerializer(product_comment)
            return custom_response('Get product comment successfully!', 'Success', serializer.data, 200)
        except:
            return custom_response('Get product comment failed!', 'Error', "Product comment not found!", 400)

    def put(self, request, product_id_slug, id_slug):
        try:
            data = parse_request(request)
            product_comment = self.get_object_with_product_id(product_id_slug, id_slug)
            serializer = ProductCommentSerializer(product_comment, data=data)
            if serializer.is_valid():
                serializer.save()
                return custom_response('Update product comment successfully!', 'Success', serializer.data, 200)
            else:
                return custom_response('Update product comment failed', 'Error', serializer.errors, 400)
        except:
            return custom_response('Update product comment failed', 'Error', "Product comment not found!", 400)

    def delete(self, request, product_id_slug, id_slug):
        try:
            product_comment = self.get_object_with_product_id(product_id_slug, id_slug)
            product_comment.delete()
            return custom_response('Delete product comment successfully!', 'Success', {"product_comment_id": id_slug},
                                   204)
        except:
            return custom_response('Delete product comment failed!', 'Error', "Product comment not found!", 400)

# example API for testing : http://127.0.0.1:8000/api/v1/filter?category_id=49&order_by=price&order_type=asc&price__gte=0.1&price__lte=0.6&name=Possible main American
class ProductFilterViewAPI(views.APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            base_queryset = Product.objects.filter(is_public=True, amount__gt=0)
            filtered_queryset = self.filter_and_paginate(request, base_queryset)
            serialize_data = ProductSerializer(filtered_queryset['queryset'], many=True).data
            result_set = {'list': serialize_data, 'pagination': filtered_queryset['pagination']}
            return custom_response('Get products successfully!', 'Success', result_set, 200)
        except Exception as e:
            return custom_response('Get product failed!', 'Error', [str(e)], 400)

    def filter_and_paginate(self, request, queryset):
        price_gte = request.GET.get('price__gte')
        price_lte = request.GET.get('price__lte')
        category_id = request.GET.get('category_id')
        name = request.GET.get('name')

        if price_gte:
            queryset = queryset.filter(price__gte=float(price_gte))
        if price_lte:
            queryset = queryset.filter(price__lte=float(price_lte))
        if category_id:
            queryset = queryset.filter(category_id=int(category_id))
        if name:
            queryset = queryset.filter(name__icontains=name)

        # SORT
        order_by_field = request.GET.get('order_by', 'id')
        order_type = request.GET.get('order_type', 'desc')
        order_by = order_by_field if order_type == 'asc' else '-' + order_by_field
        queryset = queryset.order_by(order_by)

        # PANIGATE
        per_page = int(request.GET.get('per_page', 20))
        page_no = int(request.GET.get('page_no', 1))

        paginator = Paginator(queryset, per_page)
        try:
            page = paginator.page(page_no)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)

        dataset = {
            'queryset': page.object_list,
            'pagination': {
                'per_page': per_page,
                'current_page': page_no,
                'total_count': paginator.count,
                'total_pages': paginator.num_pages
            }
        }
        return dataset
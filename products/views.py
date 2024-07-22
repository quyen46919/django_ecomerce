from rest_framework import views
from rest_framework.permissions import AllowAny
from django.http import Http404
from django.contrib.auth import get_user_model
from backend_ecommerce.helpers import custom_response, parse_request
from .models import Category, Product, ProductImage, ProductComment
from .serializers import CategorySerializer, ProductSerializer, ProductImageSerializer, ProductCommentSerializer
from filter_and_pagination import FilterPagination

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
class WishlistCheckAPIView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            product_ids = request.query_params.getlist('product_ids')
            if not product_ids:
                return custom_response('Product IDs not provided!', 'Error', None, 400)

            product_ids = [int(pid) for pid in product_ids]
            products = Product.objects.filter(id__in=product_ids, amount__gt=0, is_public=True)
            serialize_data = ProductSerializer(products, many=True).data

            # check product 
            available_products = Product.objects.filter(id__in=product_ids, amount__gt=0, is_public=True)
            unavailable_products = Product.objects.filter(id__in=product_ids).exclude(amount__gt=0, is_public=True)

            available_serialize_data = ProductSerializer(available_products, many=True).data
            unavailable_serialize_data = ProductSerializer(unavailable_products, many=True).data

            result_set = {
                'available_products': available_serialize_data,
                'unavailable_products': unavailable_serialize_data
            }
            return custom_response('Products checked successfully!', 'Success', result_set, 200)
        except Exception as e:
            return custom_response('Product check failed!', 'Error', [str(e)], 400)
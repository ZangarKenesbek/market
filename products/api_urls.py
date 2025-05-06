from django.urls import path, include
from rest_framework.routers import DefaultRouter

from django.urls import path
from .api_views import *
urlpatterns = [
    path('silk/', include('silk.urls', namespace='silk')),

    path('vacancies/', VacancyListCreateAPIView.as_view()),
    path('categories/', CategoryListCreateAPIView.as_view()),

    path('categories/<int:pk>/', CategoryDetailAPIView.as_view(), name='category-detail'),
    # path('categories/<int:pk>', CategoryRetrieveAPIView.as_view()),

    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
    # path('products/<int:pk>/', ProductRetrieveAPIView.as_view(), name='product-detail'),


    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products/<int:pk>/comments/', ProductCommentListAPIView.as_view(), name='product-review-list'),
    path('products/<int:product_pk>/comments/<int:comments_pk>/', ProductCommentsDetailAPIView.as_view(), name='product-review-detail'),
    path('comments/', CommentListCreateAPIView.as_view()),
]


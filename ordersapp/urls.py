from django.urls import path
import ordersapp.views as ordersapp

app_name = 'ordersapp'

urlpatterns = [
    path('', ordersapp.OrderList.as_view(), name='main'),
    path('forming/complete/<int:pk>/', ordersapp.order_forming_complete, name='order_forming_complete'),
    path('create/', ordersapp.OrderItemCreate.as_view(), name='order_create'),
    path('read/<int:pk>/', ordersapp.OrderRead.as_view(), name='order_read'),
    path('update/<int:pk>/', ordersapp.OrderItemUpdate.as_view(), name='order_update'),
    path('delete/<int:pk>/', ordersapp.OrderDelete.as_view(), name='order_delete'),
    path('product/<int:pk>/price/', ordersapp.get_product_price),
]

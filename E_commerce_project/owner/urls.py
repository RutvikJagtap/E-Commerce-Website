from django.urls import path
from owner import views

urlpatterns = [
    path("", views.admin_login,name="admin_login"),
    path('add_item/',views.add_item,name="add_item"),
    path('view_item/',views.view_items,name="view_items"),
    path('view_orders/',views.view_orders,name="view_orders"),
    path("delete_item/",views.delete_item,name="delete_item"),
    path("logout1/", views.logout,name="logout1")
]

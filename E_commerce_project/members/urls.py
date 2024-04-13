from django.urls import path
from members import views

urlpatterns = [
    path("", views.register,name="index"),
    path('register/',views.register,name="register"),
    path('login/',views.login,name="login"),
    path("home/", views.index,name="home"),
    path('shop/',views.shop,name="shop"),
    path('blog/',views.blog,name="blog"),
    path('about/',views.about,name="about"),
    path('contact/',views.contact,name="contact"),
    path('cart/',views.view_cart,name="cart"),
    path('user/',views.user,name="user"),
    path('add_to_cart/',views.add_to_cart,name="add_to_cart"),
    path('delete_from_cart/',views.delete_from_cart,name="delete_from_cart"),
    path('check_out/',views.check_out,name="check_out"),
    path('order_placed/',views.order_placed,name="order_placed"),
    path('update_cart/',views.update_cart,name="update_cart"),
    path('logout/',views.logout,name="logout"),
    path('forget_password/',views.forgot_password,name="forgot_password"),
    path('reset_password/',views.reset_password,name="reset_password"),
    path('sproduct/<slug:product_id>/',views.sproduct,name="sproduct")
]

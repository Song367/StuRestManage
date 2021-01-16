from django.urls import path
from django.conf.urls import url
from rest import views


urlpatterns = [
    path("createcanteen/",views.create_canteen),
    path("querycanteen/",views.query_canteen),
    path("logincanteen/",views.login_canteen),

    path("createstore/",views.create_store),
    path("updatestore/",views.update_store),
    url(r"removestore/",views.remove_store),
    path("querystore/",views.query_store),

    url("deletefood/", views.remove_food),
    path("queryfood/",views.query_food_store_by_id),
    path("insertfood/",views.insert_food),
    path("updatefood/", views.update_food),

    path("insertlogin/",views.login_insert),
    path("querylogin/",views.query_quantity),
    url("removelogin/",views.delete_login),
]
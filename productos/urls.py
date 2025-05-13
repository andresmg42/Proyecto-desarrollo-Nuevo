from django.urls import path,include
from .import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import  routers


router=routers.DefaultRouter()

router.register(r'productos',views.ProductoView,'productos')
router.register(r'users_products', views.ProductosUsuariosView,'users_products')
router.register(r'favoritos', views.FavoritosView,'favoritos')

urlpatterns = [

    path("api/",include(router.urls)),
    path("api/filter_products/", views.search_products),
    path("api/search_users_products/", views.search_users_products),
    path("api/delete_all_userProducts/",views.delete_all_user_products)
    
    

    
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


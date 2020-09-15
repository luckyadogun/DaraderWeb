from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import RegisterView, LoginView, PropertyView, HotelView, UserView, BookmarkHotelView, BookmarkPropertyView

urlpatterns = [
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('me/', UserView.as_view(), name='user'),
    path('properties/', PropertyView.as_view(), name='properties'),
    path('hotels/', HotelView.as_view(), name='hotels'),
    path('bookmark/hotel/', BookmarkHotelView.as_view(), name='bookmark-hotel'),
    path('bookmark/property/', BookmarkPropertyView.as_view(), name='bookmark-property'),
]
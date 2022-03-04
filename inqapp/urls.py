from django.urls import path
from django.conf.urls import url,include
from inqapp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('signup/', views.RegistrationView.as_view(), name='signup'),
    path('signin/', views.LoginView.as_view(), name='signin'),
    path('logout/', views.LogoutView.as_view(),name='logout'),
    path('contact-us/',views.contact,name='contact'),
    path('team-detail/',views.TeamDetailView.as_view(),name='team-detail'),
    path('', views.home,name='home'),
    path('product/', views.question,name='product'),    
    path('product-allot/', views.productAllot,name='product-allot'),    
    url('nopage',views.noPage, name="404")
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

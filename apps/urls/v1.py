from django.urls import path, include

app_name = 'v1'

urlpatterns = [
    path('users/', include('apps.users.urls.v1', namespace='users')),
    path('shared/', include('apps.shared.urls.v1', namespace='shared')),
    path('services/', include('apps.services.urls.v1', namespace='services')),
    path('about/', include('apps.about.urls.v1', namespace='about')),
    path('blogs/', include('apps.blogs.urls.v1', namespace='blogs')),
    path('contact/', include('apps.contact.urls.v1', namespace='contact')),
]
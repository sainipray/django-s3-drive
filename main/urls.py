from django.urls import path, re_path

from main.views import ListS3View

app_name = 'cloud'
urlpatterns = [
	path('', ListS3View.as_view(), name='init_url'),
	path('<directory>/', ListS3View.as_view(), name='url'),
]

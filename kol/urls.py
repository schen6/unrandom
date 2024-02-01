from django.urls import re_path, path
from kol import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('profile/', views.ProfileApi),
    # re_path(r'profile/([0-9]+)$', views.ProfileApi),
    # re_path(r'profile/$', views.ProfileApi),
    path('autocomplete/', views.autocomplete_search),
    path('post/', views.PostApi),
    path('analytics/group/', views.group_post_analytics_view),
    path('analytics/translate/', views.get_translate),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# re_path(r'api/kolbasicdata$', views.KolBasicDataApi),
# re_path(r'api/kolbasicdata/([0-9]+)$', views.KolBasicDataApi),

# re_path(r'api/brand$', views.brand_api),
# re_path(r'api/brand/([0-9]+)$', views.brand_api),
#
# re_path(r'api/attribute$', views.attribute_api),
# re_path(r'api/attribute/([0-9]+)$', views.attribute_api),
#
# re_path(r'api/product$', views.product_api),
# re_path(r'api/product/([0-9]+)$', views.product_api),
#
# re_path(r'api/kolbasicdata/savefile', views.SaveFile)
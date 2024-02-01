from django.urls import path, include
from rest_framework.routers import DefaultRouter
from groups.views import GroupViewSet, GroupKOLAssociationViewSet, GetGroupDetail, GetGroupPostDetail
from django.conf.urls.static import static
from django.conf import settings

router = DefaultRouter()
router.register(r'groups', GroupViewSet)
# router.register(r'group-detail', GroupDetailViewSet)
router.register(r'group-kol-associations', GroupKOLAssociationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('group-detail/', GetGroupDetail),
    path('group-posts/', GetGroupPostDetail),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
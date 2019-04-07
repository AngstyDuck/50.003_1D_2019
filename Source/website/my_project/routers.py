from rest_framework import routers
from vue_login.viewsets import ArticleViewSet

router = routers.DefaultRouter()

router.register(r’vue_login’, ArticleViewSet)

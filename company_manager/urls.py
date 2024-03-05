from rest_framework import routers

from company_manager.views import EnterpriseViewSet, ProductViewSet , UserViewSet
from company_manager.views.category import CategoryViewSet
from company_manager.views.order import OrderViewSet
from company_manager.views.user import UserTypeViewSet

router = routers.DefaultRouter()

router.register('product', ProductViewSet , 'products')
router.register('user', UserViewSet , 'user')
router.register('user-type', UserTypeViewSet , 'usertypes')
router.register('enterprise', EnterpriseViewSet , 'enterprise')
router.register('category', CategoryViewSet , 'category')
router.register('order', OrderViewSet , 'order')

urlpatterns = router.urls
from django.urls import path
from .views import stk_push, create_account_view,confirmation_view, validation_view, stk_callback


urlpatterns =[
  path("api/stk_push/",stk_push, name="transaction"),
  path("api/create_user/",create_account_view, name="account"),
  path("api/confirmation/<str:business_id>/", confirmation_view, name="confirmation"),
  path("api/validation/<str:business_id>/", validation_view, name="validation"),
  path("api/stk_callback/<uuid:business_id>/", stk_callback, name="callback")
]
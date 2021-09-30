from django.urls import path


from . import views


urlpatterns = [
    path('import/rakuten_card', views.rakuten_card_csv, name='rakuten_card_csv'),
]
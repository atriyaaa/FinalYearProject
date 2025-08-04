from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.predict_csv, name='predict'),
    path('get_shap_plot/<str:sample_id>/', views.get_shap_plot, name='get_shap_plot'),  # ✅ Add this
    path('download_all_shap_plots/', views.download_all_shap_plots, name='download_all_shap_plots'),  # ✅ Optional
    path('health/', views.health_check, name='health_check'),  # ✅ Optional
    path('model_info/', views.model_info, name='model_info'),  # ✅ Optional
]

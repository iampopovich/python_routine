
from django.urls import path, re_path
from response_main import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.index),
    path('about/', TemplateView.as_view(template_name="about.html",
                                        extra_context={"header": "О сайте"})),
    path('extended/', TemplateView.as_view(template_name="extended.html")),
    path('contact/', TemplateView.as_view(template_name="contact.html")),
    path('details/', views.details),
    path('dates/', TemplateView.as_view(template_name="format_dates.html")),
    path('context/', TemplateView.as_view(template_name="format_context.html")),
    path('cnds/', views.conditions),
    path('iters/', views.iterators),
    path('user_form/', views.user_form),
    path('widget_form/', views.widget_form),
    path('custom_form/', views.custom_form),
    path('styles_form/', views.styles_form),
    path('all_persons/', views.all_persons),
    path('all_persons/add_person/', views.add_person),
    path('all_persons/remove_person/<int:id>', views.remove_person),
    path('all_persons/edit_person/<int:id>', views.edit_person),
    path('all_companies/', views.show_companies),
    path('company/<int:id>', views.show_company),
]

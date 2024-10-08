"""
URL configuration for TD_MatchPDF_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from TD_MatchPDF_backend_project import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path("yo/", views.yo),
    path("pdf_compare_ordine_conferma/", views.pdf_compare_ordine_e_conferma),
    path("pdf_compare_contratto_ordine/", views.pdf_compare_contratto_ordine),
]

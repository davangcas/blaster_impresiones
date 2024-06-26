from django.urls import path

from landing.views import (
    AboutView,
    ContactView,
    IndexView,
    ModelingServiceView,
    PrintServiceView,
    ProductDetailView,
    ProductsView,
    TermsAndConditionsView,
)

app_name = "landing"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("about/", AboutView.as_view(), name="about"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("print-service/", PrintServiceView.as_view(), name="print_service"),
    path("modeling-service/", ModelingServiceView.as_view(), name="modeling_service"),
    path(
        "terms-and-conditions/",
        TermsAndConditionsView.as_view(),
        name="terms_and_conditions",
    ),
    path("products-catalog/", ProductsView.as_view(), name="products"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
]

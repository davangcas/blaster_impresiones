from django.core.paginator import EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.http import JsonResponse
from django.views.generic import DetailView, ListView, TemplateView

from products.models import Category, Product


class IndexView(TemplateView):
    template_name = "landing/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home"
        context["active_section"] = "home"
        context["products"] = Product.objects.filter(
            available=True, image__isnull=False
        ).order_by("-id")[:8]
        return context


class AboutView(TemplateView):
    template_name = "landing/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Acerca de nosotros"
        context["active_section"] = "about"
        return context


class PrintServiceView(TemplateView):
    template_name = "landing/prints.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Servicio de impresión 3D"
        context["active_section"] = "services"
        return context


class ModelingServiceView(TemplateView):
    template_name = "landing/modeling.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modelado de piezas 3D"
        context["active_section"] = "services"
        return context


class TermsAndConditionsView(TemplateView):
    template_name = "landing/terms.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Términos y condiciones"
        context["active_section"] = "terms"
        return context


class ContactView(TemplateView):
    template_name = "landing/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Contacto"
        context["active_section"] = "contact"
        return context


class ProductsView(ListView):
    template_name = "landing/products.html"
    model = Product
    paginate_by = 6

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(available=True, image__isnull=False)
            .order_by("-id")
        )

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            page = self.request.GET.get("page", 1)
            search = self.request.GET.get("search", None)
            categories = self.request.GET.getlist("categories_ids[]", None)
            products_list = self.get_queryset()

            if search:
                products_list = products_list.filter(name__icontains=search)

            if categories:
                products_list = products_list.filter(categories__id__in=categories)

            paginator = self.get_paginator(products_list, self.paginate_by)

            try:
                products = paginator.page(page)
            except PageNotAnInteger:
                products = paginator.page(1)
            except EmptyPage:
                products = paginator.page(paginator.num_pages)

            data = [
                {
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "image": product.image.url,
                }
                for product in products
            ]

            return JsonResponse(
                {"products": data, "has_next": products.has_next()}, safe=False
            )
        return super().render_to_response(context, **response_kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Productos"
        context["active_section"] = "products"
        context["categories"] = (
            Category.objects.filter(is_active=True, products__isnull=False)
            .annotate(product_count=Count("products"))
            .filter(product_count__gt=0)
            .order_by("name")
        )
        return context


class ProductDetailView(DetailView):
    template_name = "landing/product_detail.html"
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.name
        context["active_section"] = "products"
        return context

from django.shortcuts import render
from .models import SiteSettings, Category, MenuItem

def home(request):
    site, _ = SiteSettings.objects.get_or_create(pk=1)

    categories = Category.objects.filter(is_active=True).order_by("order", "name")
    items = (
        MenuItem.objects.filter(is_active=True, category__is_active=True)
        .select_related("category")
        .order_by("order", "name")
    )

    grouped = {c.id: [] for c in categories}
    for it in items:
        grouped.setdefault(it.category_id, []).append(it)

    return render(request, "web/home.html", {
        "site": site,
        "categories": categories,
        "grouped": grouped,
    })


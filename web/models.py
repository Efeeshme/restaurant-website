from django.db import models

class SiteSettings(models.Model):
    name = models.CharField(max_length=120, default="Restaurant Name")
    whatsapp = models.CharField(max_length=20, default="994500000000")
    address = models.CharField(max_length=255, default="Address")
    working_hours = models.CharField(max_length=100, default="11:00 – 23:00")
    map_url = models.URLField(default="https://maps.google.com/?q=0,0", blank=True)

    def save(self, *args, **kwargs):
        self.pk = 1  # singleton
        super().save(*args, **kwargs)

    def __str__(self):
        return "Site Settings"

class Category(models.Model):
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="menu/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return f"{self.name} ({self.category})"



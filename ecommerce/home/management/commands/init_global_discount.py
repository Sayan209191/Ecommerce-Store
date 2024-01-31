from django.core.management.base import BaseCommand
from home.models import GlobalDiscount , Product

class Command(BaseCommand):
    help = 'Initialize global discount'

    def handle(self, *args, **options):
        discount = GlobalDiscount.objects.create(percentage=8)
        for product in Product.objects.all():
            product.global_discount = discount
            product.save()

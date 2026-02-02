"""
Management command to add sample products
"""
from django.core.management.base import BaseCommand
from designs.models import Product
from decimal import Decimal


class Command(BaseCommand):
    help = 'Add sample products to the database'

    def handle(self, *args, **options):
        products = [
            {
                'name': 'Kaos Cotton Combed 30s',
                'description': 'Kaos premium bahan Cotton Combed 30s, lembut dan nyaman',
                'category': 'apparel',
                'base_cost': Decimal('45000'),
            },
            {
                'name': 'Kaos Cotton Combed 24s',
                'description': 'Kaos standar bahan Cotton Combed 24s, tebal dan kuat',
                'category': 'apparel',
                'base_cost': Decimal('40000'),
            },
            {
                'name': 'Hoodie',
                'description': 'Hoodie pullover bahan fleece tebal',
                'category': 'apparel',
                'base_cost': Decimal('85000'),
            },
            {
                'name': 'Hoodie Zipper',
                'description': 'Hoodie dengan zipper depan bahan fleece',
                'category': 'apparel',
                'base_cost': Decimal('95000'),
            },
            {
                'name': 'Crewneck',
                'description': 'Sweater crewneck bahan fleece premium',
                'category': 'apparel',
                'base_cost': Decimal('80000'),
            },
            {
                'name': 'Mug Ceramic',
                'description': 'Mug keramik 11oz untuk sublimasi',
                'category': 'merchandise',
                'base_cost': Decimal('25000'),
            },
            {
                'name': 'Keychain Acrylic',
                'description': 'Gantungan kunci akrilik custom print',
                'category': 'merchandise',
                'base_cost': Decimal('15000'),
            },
        ]

        created_count = 0
        for product_data in products:
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults=product_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created: {product.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Already exists: {product.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n✅ Done! Created {created_count} new products.')
        )

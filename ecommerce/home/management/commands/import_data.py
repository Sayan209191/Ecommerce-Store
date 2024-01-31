import csv
from django.core.management.base import BaseCommand
from home.models import Product

class Command(BaseCommand):
    help = 'Import data from CSV file to database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']

        with open(csv_file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row if it exists

            for row in reader:
                try:
                    product_data = {
                        'product_id':row[0],
                        'product_name': row[1],
                        'category': row[2],
                        'subcategory': row[3],
                        'price': int(row[4]),
                        'desc': row[5],
                        'pub_date': row[6], 
                        'image': row[7],  
                    }

                    Product.objects.create(**product_data)

                except ValueError:
                    self.stderr.write(self.style.ERROR(f"Invalid price value: {row[3]} for product {row[0]}"))
                    continue

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))

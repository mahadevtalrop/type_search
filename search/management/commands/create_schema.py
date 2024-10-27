import typesense
from django.conf import settings
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Creates the Typesense collection for books'

    def handle(self, *args, **kwargs):
        # Initialize the Typesense client
        client = typesense.Client(settings.TYPESENSE_CLIENT)

        # Define the schema for the collection
        books_schema = {
            'name': 'books',
            'fields': [
                {'name': 'title', 'type': 'string'},
                {'name': 'authors', 'type': 'string[]', 'facet': True},
                {'name': 'publication_year', 'type': 'int32', 'facet': True},
                {'name': 'ratings_count', 'type': 'int32'},
                {'name': 'average_rating', 'type': 'float'}
            ],
            'default_sorting_field': 'ratings_count'
        }

        try:
            # Create the collection if it doesn't exist
            client.collections.create(books_schema)
            self.stdout.write(self.style.SUCCESS('Successfully created the collection: books'))
        except typesense.exceptions.ObjectAlreadyExists:
            self.stdout.write(self.style.WARNING('Collection already exists'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error creating collection: {e}'))

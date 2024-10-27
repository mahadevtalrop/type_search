import typesense
from django.conf import settings
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Creates the Typesense collection for Posts'

    def handle(self, *args, **kwargs):
        # Initialize the Typesense client
        client = typesense.Client(settings.TYPESENSE_CLIENT)

        # Define the schema for the collection
        posts_schema = {
            'name': 'posts',
            'fields': [
                {'name': 'content', 'type': 'string'},
                {'name': 'post_id', 'type': 'string'},
                {'name': 'author_name', 'type': 'string'},
                {'name':'published_date', 'type': 'int64'},
            ],
            'default_sorting_field': 'published_date'
        }

        try:
            # Create the collection if it doesn't exist
            client.collections.create(posts_schema)
            self.stdout.write(self.style.SUCCESS('Successfully created the collection: posts'))
        except typesense.exceptions.ObjectAlreadyExists:
            self.stdout.write(self.style.WARNING('Collection already exists'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error creating collection: {e}'))

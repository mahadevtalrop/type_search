import typesense
from django.conf import settings
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Imports books data from a JSONL file into the Typesense collection'

    def add_arguments(self, parser):
        # Command expects a JSONL file path as an argument
        parser.add_argument('jsonl_file', type=str, help='The path to the JSONL file to import')

    def handle(self, *args, **options):
        # Get the file path from command arguments
        jsonl_file_path = options['jsonl_file']

        # Initialize the Typesense client using settings
        client = typesense.Client(settings.TYPESENSE_CLIENT)

        try:
            # Open the JSONL file and read the content
            with open(jsonl_file_path, 'r') as jsonl_file:
                jsonl_content = jsonl_file.read().encode('utf-8')

            # Import the documents into the 'books' collection
            result = client.collections['books'].documents.import_(jsonl_content)

            # Print success message with result
            self.stdout.write(self.style.SUCCESS(f'Successfully imported documents: {result}'))

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f'File not found: {jsonl_file_path}'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error importing documents: {e}'))

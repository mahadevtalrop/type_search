import requests
from django.core.management.base import BaseCommand
from django.conf import settings
import typesense
from datetime import datetime
import time

class Command(BaseCommand):
    help = 'Fetches trending posts and saves them to Typesense'

    def handle(self, *args, **kwargs):
        # API URL and Bearer Token
        url = "https://developers-learn.talrop.com/api/v1/posts/?type=trending&page=1"
        bearer_token = "v1ocvCm4ywnC25RNg19MI4lBqor6Xb"  # Replace with the actual Bearer token
        
        headers = {
            'Authorization': f'Bearer {bearer_token}'
        }

        # Initialize Typesense client
        client = typesense.Client(settings.TYPESENSE_CLIENT)

        try:
            # Make the request to the API
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Check for HTTP errors

            data = response.json()

            if data.get("status_code") == 6000:
                posts_data = data.get("data", [])

                # Extract the required fields and prepare the data for Typesense
                documents = []
                for post in posts_data:
                    # Convert date_updated to Unix timestamp
                    published_date = post.get("date_updated")
                    if published_date:
                        # Parse ISO 8601 datetime string and convert to Unix timestamp
                        published_timestamp = int(datetime.strptime(published_date, "%Y-%m-%dT%H:%M:%S.%fZ").timestamp())
                    else:
                        published_timestamp = int(time.time())  # Default to current timestamp if missing

                    document = {
                        "post_id": post.get("id"),
                        "content": post.get("content", ""),
                        "published_date": published_timestamp,
                        "author_name": post.get("author", {}).get("name", ""),
                    }
                    documents.append(document)

                # Import the posts into the Typesense collection
                if documents:
                    result = client.collections['posts'].documents.import_(documents, {'action': 'upsert'})
                    self.stdout.write(self.style.SUCCESS(f'Successfully imported documents: {result}'))

            else:
                self.stdout.write(self.style.ERROR(f"Failed to fetch data: {data.get('message')}"))

        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f"Request failed: {e}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An error occurred: {e}"))

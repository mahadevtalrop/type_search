from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import typesense

def search_books(request):
    # Initialize the Typesense client using settings
    client = typesense.Client(settings.TYPESENSE_CLIENT)

    # Get the search query from the request (default to 'harry potter' if not provided)
    search_query = request.GET.get('q', 'harry potter')

    # Define the search parameters
    search_parameters = {
        'q': search_query,
        'query_by': 'title',
        'sort_by': 'ratings_count:desc'
    }

    try:
        # Perform the search request on the 'books' collection
        search_results = client.collections['books'].documents.search(search_parameters)
        
        # Return the search results as JSON
        return JsonResponse(search_results, safe=False)

    except Exception as e:
        # Handle any errors and return an appropriate message
        return JsonResponse({'error': str(e)}, status=500)


def search_posts(request):
    # Initialize the Typesense client using settings
    client = typesense.Client(settings.TYPESENSE_CLIENT)
    
    # Get the search query from the request
    query = request.GET.get('q', '')  # Default to an empty query if not provided

    # Define the search parameters
    search_parameters = {
        'q': query,
        'query_by': 'content,author_name',  # Search by both content and author name
        'sort_by': 'published_date:desc',   # Sort by published_date in descending order
    }

    try:
        # Perform the search on the 'posts' collection
        search_results = client.collections['posts'].documents.search(search_parameters)

        return JsonResponse(search_results, safe=False)

    except typesense.exceptions.TypesenseClientError as e:
        return JsonResponse({'error': str(e)}, status=500)
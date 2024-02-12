from django.shortcuts import render
from django.http import JsonResponse
from .forms import SearchForm
from .scraping import ScrapData
from django.template.loader import render_to_string


def index(request):
    form = SearchForm()
    return render(request, 'index.html', {'form': form})


def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_field = form.cleaned_data['search_query']
            max_page = form.cleaned_data['max_pages']
            scraper = ScrapData(search_field, max_page)
            scraper.scrap_books()

            # Get the result from the scraper
            while True:
                if scraper.is_scraping_complete():
                    results = scraper.get_results()
                    break

            results_html = render_to_string('results.html', {'results': results})
            # Return the results HTML as JSON response
            return JsonResponse({'results_html': results_html})
        else:
            # Form is invalid, return error messages
            return JsonResponse({'error': form.errors}, status=400)
    else:
        # Invalid request method or not AJAX, return error message
        return JsonResponse({'error': 'Invalid request'}, status=400)

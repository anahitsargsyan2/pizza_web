from django.shortcuts import render
from django.views import View
from ..models.drinks import Drinks
import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse

class DrinksView(View):
    def get(self, request):
        URL = "https://tashirpizza.am/hy/category/drinks"
        try:
            page = requests.get(URL)
            page.raise_for_status() 

            soup = BeautifulSoup(page.content, "html.parser")
            drinks = soup.find_all("div", class_="product-item")

            results = []
            for drink in drinks[:5]:
                img_tag = drink.find("div", class_="img").find("img")
                img_url = img_tag['src'] 
                
                title_tag = drink.find("a", class_="title")
                title = title_tag.get_text(strip=True) 
                
                description_tag = drink.find("p")
                description = description_tag.get_text(strip=True) 
                
                price_tag = drink.find("span", class_="price")
                price = price_tag.get_text(strip=True) 

                drink_obj, created = Drinks.objects.update_or_create(
                    title=title,
                    defaults={
                        'description': description,
                        'price': price,
                        'image_url': img_url
                    }
                )

                results.append({
                    'title': drink_obj.title,
                    'description': drink_obj.description,
                    'price': drink_obj.price,
                    'image_url': drink_obj.image_url
                })

            return JsonResponse({'drinks': results})

        except requests.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)
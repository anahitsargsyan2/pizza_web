from django.shortcuts import render
from django.views import View
from ..models.pizza import Pizza 
import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse

class PizzaView(View):
    def get(self, request):
        URL = "https://tashirpizza.am/en/category/pizza"
        try:
            page = requests.get(URL)
            page.raise_for_status() 

            soup = BeautifulSoup(page.content, "html.parser")
            pizzas = soup.find_all("div", class_="product-item")

            results = []
            for pizza in pizzas[:3]:
                img_tag = pizza.find("div", class_="img").find("img")
                img_url = img_tag['src'] 
                
                title_tag = pizza.find("a", class_="title")
                title = title_tag.get_text(strip=True) 
                
                description_tag = pizza.find("p")
                description = description_tag.get_text(strip=True) 
                
                price_tag = pizza.find("span", class_="price")
                price = price_tag.get_text(strip=True) 

                pizza_obj, created = Pizza.objects.update_or_create(
                    title=title,
                    defaults={
                        'description': description,
                        'price': price,
                        'image_url': img_url
                    }
                )

                results.append({
                    'title': pizza_obj.title,
                    'description': pizza_obj.description,
                    'price': pizza_obj.price,
                    'image_url': pizza_obj.image_url
                })

            return JsonResponse({'pizzas': results})

        except requests.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)
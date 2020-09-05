import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
page = 1
while page < 114:
    data = requests.get('http://www.horangi.kr/foodinfo/recipe.asp?page=' + str(page) + '', headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    foods = soup.select('#schlist > li')
    for idx, food in enumerate(foods):
        if idx == 0:
            a_tag = food.select_one('a')['href']
            page = page + 1
            print("http://www.horangi.kr/foodinfo/" + a_tag)
            food_html = requests.get("http://www.horangi.kr/foodinfo/" + a_tag, headers=headers)
            food = BeautifulSoup(food_html.text, 'html.parser')
            title = food.select_one('#mainTitle').text.replace('조리법/레시피','')
            image = food.select_one('#titleimg')['src']
            print(title)
            ingredients =food.select('#mainMaterial > div.mateLiCardBook > div ')
            ingredient_data = []
            for ingredient in ingredients:
                ingredient_data.append(ingredient.select_one('h3').text + '-' + ingredient.select_one('p').text)
                print(ingredient_data)


            recipes = food.select('#recipeDiv > div')
            recipe_data = []
            for recipe in recipes:
                if recipe.select_one('.stepDesc') is not None:
                    recipe_data.append(recipe.select_one('.stepDesc').text.strip())
                    print(recipe_data)
            doc = {'title': title,
                   'img': image,
                   'ingredient': ingredient_data,
                   'recipe': recipe_data}
            db.foods.insert_one(doc)
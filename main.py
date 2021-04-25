import json
from flask_login import LoginManager, current_user, login_user, login_required
from flask import Flask, request, render_template, redirect, flash, url_for
from sqlalchemy.exc import IntegrityError
from datetime import timedelta 
import random

from models import db, User, ingredient
from forms import SignUp, LogIn, AddIngredient

import requests

''' Begin boilerplate code '''

''' Begin Flask Login Functions '''
login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

''' End Flask Login Functions '''

def create_app():
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
  app.config['SECRET_KEY'] = "MYSECRET"
  login_manager.init_app(app)
  db.init_app(app)
  return app

app = create_app()
 
app.app_context().push()
db.create_all(app=app)
''' End Boilerplate Code '''

url = "https://api.spoonacular.com/recipes/findByIngredients?apiKey=d7fa7c80b72c498fb29fbc572838961d&includeNutrition=true"

headers = {
  'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
  'x-rapidapi-key': "d7fa7c80b72c498fb29fbc572838961d",
  }
random_joke = "food/jokes/random"
find = "recipes/findByIngredients"
randomFind = "recipes/random"

@app.route('/')
def index():
    return render_template('home1.html')


@app.route('/login', methods=['GET'])
def login():
  form = LogIn()
  return render_template('login.html', form=form)

@app.route('/login', methods=['POST'])
def loginAction():
  form = LogIn()
  if form.validate_on_submit(): 
      data = request.form
      user = User.query.filter_by(username = data['username']).first()
      if user and user.check_password(data['password']): 
        flash('Logged in successfully.') 
        login_user(user) 
        return redirect(url_for('index')) 
  flash('Invalid credentials')
  return redirect(url_for('index'))

@app.route('/signup', methods=['GET'])
def signup():
  form = SignUp() 
  return render_template('signup.html', form=form) 

@app.route('/signup', methods=['POST'])
def signupAction():
  form = SignUp() 
  if form.validate_on_submit():
    data = request.form 
    newuser = User(username=data['username'], email=data['email']) 
    newuser.set_password(data['password']) 
    db.session.add(newuser) 
    db.session.commit()
    flash('Account Created!')
    return redirect(url_for('index'))
  flash('Error invalid input!')
  return redirect(url_for('signup')) 


@app.route('/search') #returns search page
def search_page():
  return render_template('search.html')

    
@app.route('/recipes')
def get_recipes():
  if (str(request.args['ingridients']).strip() != ""):
      # If there is a list of ingridients -> list
      querystring = {"number":5,"ranking":1,"ignorePantry":"false","ingredients":request.args['ingridients']}
      response = requests.request("GET", url + find, headers=headers, params=querystring).json()
      # print(response)
      return render_template('recipes.html', recipes=response)
  else:
      # Random recipes
      j=random.randrange(1,20)
      querystring = {"number":1}
      requestUrl = "https://api.spoonacular.com/recipes/random?number={0}&apiKey=d7fa7c80b72c498fb29fbc572838961d".format(j)
      response = requests.request("GET", requestUrl , headers=headers).json()
      #print('came here')
      #  print(response)
      return render_template('recipes.html', recipes=response['recipes'])

@app.route('/recipe') #Display recipe details
def get_recipe():
  
  recipe_id = request.args['id']
  recipe_info_endpoint = "recipes/{0}/information".format(recipe_id)
  ingedientsWidget = "recipes/{0}/ingredientWidget".format(recipe_id)
  equipmentWidget = "recipes/{0}/equipmentWidget".format(recipe_id)
  url= 'https://api.spoonacular.com/'
  apiKey = '?apiKey=d7fa7c80b72c498fb29fbc572838961d'
  recipe_info = requests.request("GET", url + recipe_info_endpoint + apiKey, headers=headers).json()

  recipe_headers = {
      'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
      'x-rapidapi-key': "d7fa7c80b72c498fb29fbc572838961d",
      'accept': "text/html"
  }
  querystring = {"defaultCss":"true", "showBacklink":"false"}

  recipe_info['inregdientsWidget'] = requests.request("GET", url + ingedientsWidget + apiKey, headers=recipe_headers, params=querystring).text
  recipe_info['equipmentWidget'] = requests.request("GET", url + equipmentWidget +apiKey, headers=recipe_headers, params=querystring).text

 
    
  return render_template('recipe.html', recipe=recipe_info)

@app.route('/mylist', methods=['GET'])
@login_required
def myingredients():
  ingredients = ingredient.query.filter_by(userid=current_user.id).all()
  
  if ingredients is None:
      ingredients = [] 
  return render_template('mylist.html', ingredients=ingredients)
 
@app.route('/myingredients', methods=['GET']) 
@login_required
def myIngredients():
  form = AddIngredient() 
  return render_template('myingredients.html', form=form)


@app.route('/myingredients', methods=['POST']) #Add ingredient to database
@login_required
def ingredientsAction():
  
  form = AddIngredient()
  if form.validate_on_submit():
    data = request.form 
    
    ing = ingredient(name=data['name'], have=False, userid=current_user.id)
    
    db.session.add(ing) 
    db.session.commit()
    flash('Ingredient Added!') 
    return redirect('/mylist') 
  flash('Invalid data!')
  return redirect('/mylist') 

@app.route('/delete/<id>', methods=['GET'])
@login_required
def delete(id):
  ing = ingredient.query.filter_by(userid=current_user.id, id=id).first() 
  if ing:
    db.session.delete(ing)
    db.session.commit()
    flash('Ingredient Deleted!')
    return redirect('/mylist')
  flash('Unauthorized or Ingredient not found')
  return redirect('/mylist') 

app.run(host='0.0.0.0', port=8080, debug=True)
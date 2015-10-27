from flask import Flask, redirect, url_for, abort, request, render_template
app = Flask(__name__)

#Route defining Level #1

@app.route('/')
@app.route('/home/')
def home():
  return render_template('index.html')

@app.route('/recipes/')
def recipes():
  return render_template('recipes.html', currentpage="recipes") 
  
@app.route('/restaurants/')
def restaurants():
  return render_template('restaurants.html')

@app.route('/happiness/')
def happiness():
  return render_template('happiness.html')

@app.route('/fitness/')
def fitness():
  return render_template('fitness.html')

@app.route('/cats/')
def cats():
  return render_template('cats.html')

#Route defining Level #2 of Recipes

@app.route('/recipes/breakfast/')
def breakfast():
  return render_template('breakfast.html')

@app.route('/recipes/lunch/')
def lunch():
  return render_template('lunch.html')

@app.route('/recipes/snacks/')
def snacks():
  return render_template('snacks.html')

@app.route('/recipes/dinner/')
def dinner():
  return render_template('dinner.html')

@app.route('/recipes/ingredients/')
def ingredients():
  return render_template('ingredients.html',currentpage="ingredients")

#Route defining Level #2 of Restaurants

@app.route('/restaurants/bordeaux/')
def bordeaux():
  return "Bordeaux"
#  return render_template('bordeaux.html')

@app.route('/restaurants/berlin/')
def berlin():
  return "Berlin"
#  return render_template('berlin.html')

@app.route('/restaurants/nyc/')
def nyc():
  return "NYC"
#  return render_template('nyc.html')

@app.route('/restaurants/edinburgh/')
def edinburgh():
  return "Edinburgh"
#  return render_template('edinburgh.html')

@app.route('/restaurants/amsterdam/')
def amsterdam():
  return "Amsterdam"
#  return render_template('amsterdam.html')

#Route defining Level #3 Breakfast

@app.route('/recipes/breakfast/pancakes/')
def pancakes():
  ingredients = ['2 eggs', '1 cup oats', '200g yoghurt']
  toppings = ['Banana','Blueberries','Fig','Raspberries','Honey','Chocolate','Nuts']
  return render_template('pancakes.html',ingredients=ingredients,
  toppings=toppings) 
  
#Route defining Level #3 Snacks

@app.route('/recipes/snacks/sweet/')
def sweet():
#  return "Treat yourself with some of those sweet snack ideas!"
  base = ['2tbsp sunflower seeds, ground','2tbsp linseed (flax seeds), ground','2 Medjool dates']
  filling = ['1cup coconut shreds','1 banana','3tbsp lemon juice','1tbsp sweetner of choice (raw honey, maple syrup)','handful of mint','1/2 tsp + 1/3 tsp matcha green tea']
  return render_template('sweet.html',base=base,filling=filling,currentpage="sweet")

@app.route('/recipes/snacks/dips/')
def dips():
#  return "Try those dips for a quick appetizer!"
  ingredients = ['2 cups of soaked chickpeas','5tbsp of olive oil','4-6tbsp of water','ab. 10 basil leaves','the juice of 1 and 1/2 juicy lemons','2 tsp of tahini','1 tsp of cumin']
  return render_template('dips.html',ingredients=ingredients)

#Route defining Level #3 of Lunch

@app.route('/recipes/lunch/salad/')
def salad():
  ingredients = ['Green salad','Tomatoes','Feta','Smoked salmon','Soft-boiled Egg','Mais','Carrots','Taboule','Emmental']
  return render_template('salad.html',ingredients=ingredients)

#Route defining Level #3 of Dinner

@app.route('/recipes/dinner/soup/')
def soup():
  ingredients = ['2 onions chopped','1tbsp sunflower oil','1 butternut squash, peeled and diced','4 carrots, peeled and sliced','2 sprigs fresh thyme, leaves only','Salt and freshly crack black pepper','1.5 litres hot vegetable stock','Parsley for garnishing','Creme fraiche for garnishing']
  return render_template('soup.html',ingredients=ingredients)

#Route defining Level #3 Ingredients

@app.route('/recipes/ingredients/carbs/')
def carbs():
  examples = ['Brown rice', 'Wholemeal bread', 'Quinoa', 'Oats']
  return render_template('carbs.html',examples=examples)

@app.route('/recipes/ingredients/veggies/')
def veggies():
  examples = ['Salad', 'Tomatoes', 'Broccoli', 'Aubergine']
  return render_template('veggies.html',examples=examples)

@app.route('/recipes/ingredients/fruits/')
def fruits():
  examples = ['Bananas', 'Strawberries', 'Apples', 'Figs']
  return render_template('fruits.html',examples=examples)

@app.route('/recipes/ingredients/protein/')
def protein():
  examples = ['Fish', 'Poultry', 'Meat', 'Eggs']
  return render_template('protein.html',examples=examples)

@app.route('/recipes/ingredients/dairy/')
def dairy():
  examples = ['Milk', 'Yoghurt', 'Cheese']
  return render_template('dairy.html',examples=examples)

@app.route('/recipes/ingredients/healthyfats/')
def healthyfats():
  examples = ['Avocado', 'Olive oil', 'Nuts', 'Seeds']
  return render_template('healthyfats.html',examples=examples)

#Redirect

@app.route("/private")
def private():
  """Test for user logged in failed
  so redirect to login URL"""
  return redirect(url_for('login'))

@app.route('/login')
def login():
  return "Here you would be ask for your login and password"

#Error handling

@app.route('/error404')
def error404():
  abort(404)

@app.errorhandler(404)
def page_not_found(error):
  return "Sorry darling, the page you requested couldn't be found.",404

#Request

@app.route("/newsletter/", methods=['POST','GET'])
def newsletter():
  if request.method == 'POST':
    print request.form
    name = request.form['name']
    email = request.form['email']
    picture = request.files['picture']
    picture.save('static/uploads/picture.png')
    msg = "Hello %s" % name + "<br/> Thank you for signing up! A confirmation email has been sent to %s" % email + "."
    msg += "Your photo has been succesfully uploaded"
    return msg
  else:
    page = '''
    <html>
    <body>
      <form action="" method="post" name="form" enctype="multipart/form-data">
       <p> <label for="name">Name:</label>
        <input type="text" name="name" id="name"/>
       </p>
       <p> <label for="email">E-mail:</label>
        <input type="email" name="email" id="email" required/>
      </p>
      <p> <input type="file" name="picture" />
      </p>
      <p>
        <input type="submit" name="submit" id="submit" value="Submit"/>
      </p>
     </form>
    </body>
    </html>
    '''
    return page, 200 

#URL Variables
@app.route("/myaccount/")
@app.route("/myaccount/<name>")
def myaccount(name=None):
  return render_template('myaccount.html', name=name) 

#URL Parameters : Account informations

@app.route("/myaccount2/")
def myaccount2():
  name = request.args.get('name','')
  email= request.args.get('email','')
  if name == '':
    response_name = "Hi!<br/> You didn't enter your name"
  else:
    response_name = "Hi!<br/> Your name is %s" % name
  if email == '': 
    response_email = "You didn't enter your email"
  else:
    response_email = "Your email is %s" % email
  return response_name + "<br/>" + response_email

if __name__ == "__main__":
  app.run(host='0.0.0.0',debug=True)

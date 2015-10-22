from flask import Flask, redirect, url_for, abort, request, render_template
app = Flask(__name__)

#Route defining Level #1

@app.route('/')
def home():
  return "Hi this is the homepage!"

@app.route('/recipes/')
def recipes():
 # return "Here you can find a lot of cool recipes"
  return render_template('recipes.html') 
  
@app.route('/restaurants/')
def restaurants():
  return "Discover where to go next for a brunch"

@app.route('/happiness/')
def happiness():
  return "Read about changing your mindset to be happier"

#Route defining Level #2 of Recipes

@app.route('/recipes/breakfast/')
def breakfast():
#  return "Kick start your day and try some of those awesome recipes for breakfast!"
  return render_template('breakfast.html')

@app.route('/recipes/lunch/')
def lunch():
#  return "Pick some ideas for a creative lunch time!"
  return render_template('lunch.html')

@app.route('/recipes/snacks/')
def snacks():
#  return "Hungry? Try some of those snacks ideas!"
  return render_template('snacks.html')

@app.route('/recipes/dinner/')
def dinner():
#  return "Find here some cool recipes for your dinner!"
  return render_template('dinner.html')

@app.route('/recipes/ingredients/')
def ingredients():
#  return "Discover the different Food Groups :"
  return render_template('ingredients.html')

#Route defining Level #3 Breakfast

@app.route('/recipes/breakfast/pancakes/')
def pancakes():
  ingredients = ['2 eggs', '1 cup oats', '200g yoghurt']
  toppings = ['Peanut butter','Blueberries','Banana','Raspberries','Honey','Chocolate','Nuts']
  return render_template('pancakes.html',ingredients=ingredients,
  toppings=toppings) 
  
#Route defining Level #3 Snacks

@app.route('/recipes/snacks/sweet/')
def sweet():
  return "Treat yourself with some of those sweet snack ideas!"

@app.route('/recipes/snacks/dips/')
def dips():
  return "Try those dips for a quick apetizer!"

#Route defining Level #3 Ingredients

@app.route('/recipes/ingredients/carbs/')
def carbs():
  return "Carbs"

@app.route('/recipes/ingredients/veggies/')
def veggies():
  return "Veggies"

@app.route('/recipes/ingredients/fruits/')
def fruits():
  return "Fruits"

@app.route('/recipes/ingredients/protein/')
def protein():
  return "Protein"

@app.route('/recipes/ingredients/dairy/')
def dairy():
  return "Dairy"

@app.route('/recipes/ingredients/healthyfats/')
def healthyfats():
  return "Healthy Fats"

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

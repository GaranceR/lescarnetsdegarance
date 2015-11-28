#All the imports
import sqlite3
import ConfigParser
import logging
import os

from logging.handlers import RotatingFileHandler
from flask import Flask, redirect, url_for, abort, request, render_template, \
session, g, flash
from flask.ext.login import LoginManager, UserMixin, login_required,\
login_user, logout_user, current_user
from flask.ext.wtf import Form

from wtforms import TextField, HiddenField
from contextlib import closing

from urlparse import urlparse, urljoin

#Create the app
app = Flask(__name__)

#Login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
#was useless?? take id as a parameter to find the id ....
  c = g.db.execute("SELECT * FROM user WHERE id_user = (?)", [id])
  user = c.fetchone()
  return user

class User(UserMixin): 

  def __init__(self,username,password,email):
    self.username = username
    self.password = password
    self.email = email

  def is_authenticated(self):
    return True

  def is_active(self):
    return True

  def is_anonymous(self):
    return False

  #might be useless? since we have load_user() ?
  def get_id(self):
    c = g.db.execute('SELECT id_user FROM user WHERE name_user = (?)',\
    [self.username])
    id = c.fetchone()
    return unicode(id)

  def __repr__(self):
    return '<User %r>' % (self.username)

#Functions

def init(app):
  config = ConfigParser.ConfigParser()
  config_location = "etc/config.cfg"
  try: 
    config.read(config_location)

    app.config['debug'] = config.get("config","debug")
    app.config['ip_address'] = config.get("config","ip_address")
    app.config['port'] = config.get("config","port")
    app.config['url'] = config.get("config","url")

    app.config['database'] = config.get("config","database")
    app.config['username'] = config.get("config","username")
    app.config['password'] = config.get("config","password")

    app.config['log_file'] = config.get("logging","name")
    app.config['log_location'] = config.get("logging","location")
    app.config['log_level'] = config.get("logging","level")
    
    app.secret_key = config.get("config","secret_key")

  except:
    print "Could not read configs from:", config_location

def logs(app):
  log_pathname = app.config['log_location'] + app.config['log_file']
  file_handler = RotatingFileHandler(log_pathname, maxBytes=1024*1024*10,backupCount=1024)
  file_handler.setLevel(app.config['log_level'])
  formatter = logging.Formatter("%(levelname)s | %(asctime)s | %(module)s |\
  %(funcName)s | %(message)s")
  file_handler.setFormatter(formatter)
  app.logger.setLevel(app.config['log_level'])
  app.logger.addHandler(file_handler)

def connect_db():
  init(app)
  conn = sqlite3.connect(app.config['database'])
  conn.row_factory = sqlite3.Row
  return conn

def init_db():
  with closing(connect_db()) as db:
    with app.open_resource('schema.sql', mode='r') as f:
      db.cursor().executescript(f.read())
    db.commit()

def get_db():
  if not hasattr(g, 'sqlite_db'):
    g.sqlite_db = connect_db()
  return g.sqlite_db

def query_db(query, args=(), one = False):
  cur = g.db.execute(query, args)
  rv = [dict((cur.description[idx][0], value)
    for idx, value in enumerate(row)) for row in cur.fetchall()]
  return (rv[0] if rv else None) if one else rv

def get_recipe(id):
  query = 'SELECT * FROM recipe WHERE id_recipe = ?'
  recipe = query_db(query, [id], one = True)
  return recipe

@app.before_request
def before_request():
  #g.user = current_user
  g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
  db = getattr(g,'db', None)
  if db is not None:
    db.close()

@app.route('/display_users')
def display_users():
  cur = g.db.cursor()
  cur = g.db.execute('SELECT id_user, name_user, email_user FROM user ORDER BY id_user ASC')
  entries = [dict(id_user=row[0],name_user=row[1], email_user=row[2]) for row in cur.fetchall()]
  return render_template('display_users.html',entries=entries, currentpage =\
  "display_users")

@app.route('/createaccount/', methods=['GET','POST'])
def createaccount():
  if request.method == 'GET':
    return render_template('createaccount.html')
  #error = None
  if request.method == 'POST':
    db = get_db()
    #INSERT in DB
    db.execute('INSERT INTO user (name_user, password_user, email_user) VALUES \
    (?,?,?)',[request.form['username'],request.form['password'],request.form['email']])
    db.commit()
    flash('Your account was successfully created!')
    #return redirect(url_for('home')) 
    return render_template('index.html',previouspage="createaccount") 

def is_safe_url(target):
  ref_url = urlparse(request.host_url)
  test_url = urlparse(urljoin(request.host_url, target))
  return test_url.scheme in ('http','https') and \
    ref_url.netloc == test_url.netloc

def get_redirect_target():
  for target in request.args.get('next'), request.referrer:
    if not target:
      continue
    if is_safe_url(target):
      return target

class RedirectForm(Form):
  next = HiddenField()

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
    if not self.next.data:
      self.next.data = get_redirect_target() or ''

  def redirect(self, endpoint='index', **values):
    if is_safe_url(self.next.data):
      return redirect(self.next.data)
    target = get_redirect_target()
    return redirect(target or url_for(endpoint, **values))

class LoginForm(RedirectForm):
  username = TextField('Username')
  password = TextField('Password')

@app.route('/login', methods = ['GET','POST'])
def login():
  error = None
  form = LoginForm()
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    #if form.validate_on_submit():
    c = g.db.execute("SELECT name_user FROM user WHERE name_user = (?)",[username])
    userexists = c.fetchone()
    if userexists: 
      c = g.db.execute("SELECT password_user FROM user WHERE \
        password_user = (?)", [password])
      passwcorrect = c.fetchone()
    else:
      return render_template('login.html',error = 'Invalid username')
    if passwcorrect:
      user = User(username,password,'email')
      login_user(user)
      session['logged_in'] = True 
      flash('Logged in successfully.')
      #return redirect(url_for('home',msg=msg))
      return render_template('index.html',user=user,previouspage="login")
    else:
      error = 'Invalid password'
    '''
    next = request.args.get('next')
    if not next_is_valide(next):
      return abort(400)
    return redirect(next or url_for('index'))
    '''
  return render_template('login.html',form=form,error=error)

@app.route('/logout')
#@login_required
def logout():
  logout_user()
  session['logged_in'] = False
  #session.pop('logged_in', None)
  flash('You were logged out')
  return redirect(url_for('home'))

@app.route('/addfavs', methods=['GET','POST'])
def add_to_favs():
  if not session.get('logged_in'):
    abort(401)
  if request.method == 'POST':
    #FIND ID CURRENT USER
    #iduser = current_user.get_id(current_user)
    #INSERT IN DB
    db = get_db()
    db.execute('INSERT INTO list_recipe (id_user, id_recipe, etat, favourite) VALUES \
    (%s,%s,"%s",%s)' % (1,1,"love it",1))
    #[iduser],[idrecipe]
    db.commit()
    #Exemple of Pancakes
    id = 1
    recipe = get_recipe(id)
    flash('Thanks, this recipe has been added to your favourite!')
    #For now only Example of Pancakes working
    return render_template('pancakes.html',recipe=recipe)


#Route defining Level #1
@app.route('/')
@app.route('/home/')
def home():
  msg = None
  #if 'username' in session:
    #msg='Logged in as %s' % escape(session['username'])
  #else:
    #msg='You are not logged in'
  #user = None
  #if current_user.is_authenticated:
    #current_user = true;
  user = load_user(1)
  c = g.db.execute('SELECT name_user FROM user WHERE id_user = 1')
  #[user.id_user])
  #useless?
  username = c.fetchone()
  return render_template('index.html', msg=msg, user=user, currentpage="home")

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
@app.route('/recipes/breakfast/pancakes/<int:id>')
def pancakes(id=None):
  #ingredients = ['2 eggs', '1 cup oats', '200g yoghurt']
  #toppings = ['Banana','Blueberries','Fig','Raspberries','Honey','Chocolate','Nuts']
  recipe = get_recipe(id)
  #only working for one example so far
  #id = recipe['id_recipe']
  #query = 'SELECT * FROM recipe'
  return render_template('pancakes.html', recipe = recipe)
  #return render_template('pancakes.html',ingredients=ingredients,
  #toppings=toppings, recipe=recipe)

  
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
    msg += "<img src='/static/uploads/picture.png' alt='your image'title='title of your image'/>"
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
  init(app)
  logs(app)
  app.run(
    debug=app.config['debug'],
    host=app.config['ip_address'],
    port=int(app.config['port'])
    )

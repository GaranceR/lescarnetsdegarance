from flask import Flask, redirect, url_for, abort
app = Flask(__name__)

#Route defining Level #1

@app.route('/')
def home():
  return "Hi this is the homepage!"

@app.route('/recipes/')
def recipes():
  return "Here you can find a lot of cool recipes"

@app.route('/recipes/breakfast/pancakes/')
def pancakes():
  start = '<img src="'
  url = url_for('static', filename='pancakes.PNG')
  end = '">'
  return start+url+end,200

@app.route('/restaurants/')
def restaurants():
  return "Discover where to go next for a brunch"

@app.route('/happiness/')
def happiness():
  return "Read about changing your mindset to be happier"

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

if __name__ == "__main__":
  app.run(host='0.0.0.0',debug=True)

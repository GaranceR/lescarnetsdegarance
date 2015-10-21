from flask import Flask, redirect, url_for, abort, request
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

@app.route("/myaccount/<name>")
def myaccount(name):
  return "Your name is %s" % name

#URL Parameters : Account informations

@app.route("/myaccount2/")
def myaccount2():
  name = request.args.get('name','')
  email= request.args.get('email','')
  if name == '':
    response_name = "You didn't enter your name"
  else:
    response_name = "Hi!<br/> Your name is %s" % name
  if email == '': 
    response_email = "You didn't enter your email"
  else:
    response_email = "Your email is %s" % email
  return response_name + "<br/>" + response_email

if __name__ == "__main__":
  app.run(host='0.0.0.0',debug=True)

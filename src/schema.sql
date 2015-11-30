DROP TABLE if EXISTS user;

CREATE TABLE user (
 id_user integer PRIMARY KEY autoincrement,
 name_user varchar(30) NOT NULL,
 password_user varchar(30) NOT NULL,
 email_user varchar(30) NOT NULL
);

DROP TABLE if EXISTS recipe;

CREATE TABLE recipe (
  id_recipe integer PRIMARY KEY autoincrement,
  title_recipe varchar(100) NOT NULL,
  ingredients_recipe text[],
  addings_recipe text[],
  directions_recipe text NOT NULL
);

DROP TABLE if EXISTS foodgroup;

CREATE TABLE foodgroup (
  id_foodgroup integer PRIMARY KEY autoincrement,
  title_foodgroup varchar(100) NOT NULL,
  examples_foodgroup text[],
  description_foodgroup text NOT NULL
);

DROP TABLE if EXISTS list_recipe;

CREATE TABLE list_recipe (
  id_user integer,
  id_recipe integer,
  etat text NOT NULL,
  favourite boolean DEFAULT 0,
  FOREIGN KEY(id_user) REFERENCES user(id_user),
  FOREIGN KEY(id_recipe) REFERENCES recipe(id_recipe)
);


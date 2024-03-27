# Databases

- right click on databases new database
- right click for new query

# connecting strings for database  

- go to connection strings
- click on ODBC connection string

# ORM 
- auto complete
- it easy to work with data types
- multiple databases  - if you change database you don't have to change all the code 
- DX

Blueprint
model 
template
source

# Template inheritance 
certain parts of the app to share the view layer everywhere 
- Share view [Header, footer]

base html
```html
<html>
    <header></header>
    {% block green_box %}
    {% endBlock %}

    {% block red_box %}
    {% endBlock %}
    <footer></footer>
<html>
```
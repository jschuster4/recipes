import re
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.recipes import Recipe

@app.route("/recipes/create")
def display_new_recipe_page(): 
    return render_template("create_recipe.html")

@app.route("/recipes/new", methods= ['POST'])
def add_recipe(): 
    if Recipe.validate_recipe(request.form):
        data = {
            'name' : request.form['name'],
            'description' : request.form['description'],
            'instruction' : request.form['instruction'],
            'under_30_minutes' : request.form['under_30_minutes'],
            'id' : session['user_id'],
            'date_made_on' : request.form['date']
        }
        new_recipe = Recipe.add_recipe(data)
        return redirect("/success")
    else: 
        return redirect("/recipes/create")

@app.route("/recipes/<int:recipe_id>")
def view_recipe(recipe_id):
    if 'user_id' not in session:
        flash("You must be logged in to view this page")
        return redirect("/")
    data = {
        'id' : recipe_id
    }
    one_recipe = Recipe.get_one_recipe(data)
    return render_template("recipe_instance.html", one_recipe = one_recipe)

@app.route("/recipes/edit/<int:recipe_id>")
def edit_recipe_page(recipe_id):
    if 'user_id' not in session:
        flash("You must be logged in to view this page")
        return redirect("/")
    data = {
        'id' : recipe_id
    }
    one_recipe = Recipe.get_one_recipe(data)
    return render_template("edit_recipe.html", one_recipe = one_recipe)

#route to delete a user
@app.route("/recipes/delete/<int:recipe_id>")
def delete_user(recipe_id):
    data = {
        'id' : recipe_id
    }
    Recipe.delete_recipe(data)
    return redirect('/success')

@app.route("/recipes/update/<int:recipe_id>", methods = ['POST'])
def update_recipe(recipe_id):
    if Recipe.validate_recipe(request.form):
        data = {
            'id' : recipe_id,
            'name' : request.form['name'],
            'description' : request.form['description'],
            'instruction' : request.form['instruction'],
            'under_30_minutes' : request.form['under_30_minutes'],
            'user_id' : session['user_id'],
            'date_made_on' : request.form['date']
        }
        Recipe.update_recipe(data)
        return redirect("/success")
    else: 
        return redirect(f"/recipes/edit/{recipe_id}")


from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Recipe:
    def __init__(self,data): 
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.under_30_minutes = data['under_30_minutes']
        self.instruction = data['instruction']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.date_made_on = data['date_made_on']
        self.user_id = data['user_id']
        self.user = {}
    
    @classmethod
    def add_recipe(cls, data):
        query = "INSERT INTO recipes (name, description, under_30_minutes, instruction, created_at, updated_at, user_id, date_made_on) VALUES(%(name)s, %(description)s, %(under_30_minutes)s, %(instruction)s, NOW(), NOW(), %(id)s, %(date_made_on)s );"
        results = connectToMySQL('recipes').query_db(query, data)
        return results

    @classmethod
    def get_one_recipe(cls,data): 
        query = "SELECT * FROM recipes WHERE id= %(id)s;"
        results = connectToMySQL('recipes').query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes"
        results = connectToMySQL('recipes').query_db(query)
        recipes = []
        for item in results: 
            recipes.append( cls(item))
        return recipes

    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL('recipes').query_db(query, data)
        
    @classmethod
    def update_recipe(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, under_30_minutes = %(under_30_minutes)s, instruction = %(instruction)s, updated_at = NOW(), date_made_on = %(date_made_on)s WHERE id= %(id)s"
        results = connectToMySQL('recipes').query_db(query, data)
        # dont return anything for update or delete
    
    @staticmethod
    def validate_recipe(data): 
        is_valid = True

        # confirm that the first name length is between 3 and 30 characters
        if len(data["name"]) < 3 or len(data["name"]) > 30:
            is_valid = False
            flash("name must be at least 3 characters, and at most 30 characters")

        # confirm that the last name length is between 3 and 30 characters
        if len(data["description"]) < 3 or len(data["description"]) > 45:
            is_valid = False
            flash("description must be at least 3 characters, and at most 45 characters")

        if len(data["instruction"]) < 3 or len(data["instruction"]) > 45:
            is_valid = False
            flash("")

        if data["date"] == "": 
            is_valid = False

        if not "under_30_minutes" in data:
            is_valid = False
            flash("")


        return is_valid

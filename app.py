from flask import Flask, render_template, request
from random import uniform as rnd
import pandas as pd

# Assuming get_images_links is a function from ImageFinder module that fetches image links
from ImageFinder import get_images_links as find_image

app = Flask(__name__)

recipes_df = pd.read_csv('recipes.csv')

class Generator:
    def __init__(self, nutrition_input: list):
        self.nutrition_input = nutrition_input

    def generate(self):
        # Use the recipes dataset to generate recipes
        sample_recipes = recipes_df.sample(n=3).to_dict(orient='records')  # Sample 3 recipes
        for recipe in sample_recipes:
            recipe['Calories'] = self.nutrition_input[0]
            recipe['image_link'] = find_image(recipe['Name'])
        return {"output": sample_recipes}

class Person:
    def __init__(self, age, height, weight, gender, activity, meals_calories_perc, weight_loss):
        self.age = age
        self.height = height
        self.weight = weight
        self.gender = gender
        self.activity = activity
        self.meals_calories_perc = meals_calories_perc
        self.weight_loss = weight_loss

    def calculate_bmi(self):
        bmi = round(self.weight / ((self.height / 100) ** 2), 2)
        return bmi

    def display_result(self):
        bmi = self.calculate_bmi()
        if bmi < 18.5:
            category = 'Underweight'
            color = 'Red'
        elif 18.5 <= bmi < 25:
            category = 'Normal'
            color = 'Green'
        elif 25 <= bmi < 30:
            category = 'Overweight'
            color = 'Yellow'
        else:
            category = 'Obesity'
            color = 'Red'
        return bmi, category, color

    def calculate_bmr(self):
        if self.gender == 'Male':
            bmr = 10 * self.weight + 6.25 * self.height - 5 * self.age + 5
        else:
            bmr = 10 * self.weight + 6.25 * self.height - 5 * self.age - 161
        return bmr

    def calories_calculator(self):
        activities = ['Little/no exercise', 'Light exercise', 'Moderate exercise (3-5 days/wk)', 'Very active (6-7 days/wk)', 'Extra active (very active & physical job)']
        weights = [1.2, 1.375, 1.55, 1.725, 1.9]
        weight = weights[activities.index(self.activity)]
        maintain_calories = self.calculate_bmr() * weight
        return maintain_calories

    def generate_recommendations(self):
        total_calories = self.weight_loss * self.calories_calculator()
        recommendations = []
        for meal in self.meals_calories_perc:
            meal_calories = self.meals_calories_perc[meal] * total_calories
            recommended_nutrition = [
                meal_calories, rnd(10, 40), rnd(0, 4), rnd(0, 30), rnd(0, 400), rnd(40, 75), rnd(4, 20), rnd(0, 10), rnd(30, 175)
            ]
            generator = Generator(recommended_nutrition)
            recommended_recipes = generator.generate()['output']
            for recipe in recommended_recipes:
                recipe['image_link'] = find_image(recipe['Name'])
            recommendations.append(recommended_recipes)
        return recommendations

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        age = int(request.form.get('age'))
        height = int(request.form.get('height'))
        weight = int(request.form.get('weight'))
        gender = request.form.get('gender')
        activity = request.form.get('activity')
        weight_loss_option = request.form.get('weight_loss_option')
        number_of_meals = int(request.form.get('number_of_meals'))

        plans = ["Maintain weight", "Mild weight loss", "Weight loss", "Extreme weight loss"]
        weights = [1, 0.9, 0.8, 0.6]
        weight_loss = weights[plans.index(weight_loss_option)]

        if number_of_meals == 3:
            meals_calories_perc = {'breakfast': 0.35, 'lunch': 0.40, 'dinner': 0.25}
        elif number_of_meals == 4:
            meals_calories_perc = {'breakfast': 0.30, 'morning snack': 0.05, 'lunch': 0.40, 'dinner': 0.25}
        else:
            meals_calories_perc = {'breakfast': 0.30, 'morning snack': 0.05, 'lunch': 0.40, 'afternoon snack': 0.05, 'dinner': 0.20}

        person = Person(age, height, weight, gender, activity, meals_calories_perc, weight_loss)
        bmi, category, color = person.display_result()
        maintain_calories = person.calories_calculator()

        recommendations = person.generate_recommendations()
        return render_template('results.html', bmi=bmi, category=category, color=color, maintain_calories=maintain_calories,
                               weight_loss_option=weight_loss_option, recommendations=recommendations)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

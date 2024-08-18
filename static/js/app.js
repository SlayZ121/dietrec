document.addEventListener('DOMContentLoaded', () => {
    const root = document.getElementById('root');

    const createForm = () => {
        return `
            <div class="container">
                <header>
                    <h1>Automatic Diet Recommendation</h1>
                </header>
                <form id="recommendation-form">
                    <label for="age">Age:</label>
                    <input type="number" id="age" name="age" min="2" max="120" required>
                    <label for="height">Height (cm):</label>
                    <input type="number" id="height" name="height" min="50" max="300" required>
                    <label for="weight">Weight (kg):</label>
                    <input type="number" id="weight" name="weight" min="10" max="300" required>
                    <label for="gender">Gender:</label>
                    <select id="gender" name="gender" required>
                        <option value="Male">Male</option>
                        <option value="Female">Female</option>
                    </select>
                    <label for="activity">Activity:</label>
                    <select id="activity" name="activity" required>
                        <option value="Little/no exercise">Little/no exercise</option>
                        <option value="Light exercise">Light exercise</option>
                        <option value="Moderate exercise (3-5 days/wk)">Moderate exercise (3-5 days/wk)</option>
                        <option value="Very active (6-7 days/wk)">Very active (6-7 days/wk)</option>
                        <option value="Extra active (very active & physical job)">Extra active (very active & physical job)</option>
                    </select>
                    <label for="weight-loss-plan">Weight Loss Plan:</label>
                    <select id="weight-loss-plan" name="weight_loss_plan" required>
                        <option value="Maintain weight">Maintain weight</option>
                        <option value="Mild weight loss">Mild weight loss</option>
                        <option value="Weight loss">Weight loss</option>
                        <option value="Extreme weight loss">Extreme weight loss</option>
                    </select>
                    <label for="meals-per-day">Meals per Day:</label>
                    <input type="number" id="meals-per-day" name="meals_per_day" min="3" max="5" required>
                    <button type="submit">Get Recommendations</button>
                </form>
                <div id="recommendations"></div>
            </div>
        `;
    };

    root.innerHTML = createForm();

    const form = document.getElementById('recommendation-form');
    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = new FormData(form);
        const data = {
            age: formData.get('age'),
            height: formData.get('height'),
            weight: formData.get('weight'),
            gender: formData.get('gender'),
            activity: formData.get('activity'),
            weight_loss: formData.get('weight_loss_plan'),
            meals_calories_perc: {
                breakfast: 0.3,
                lunch: 0.4,
                dinner: 0.3
            }
        };

        try {
            const response = await fetch('/recommend', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            const result = await response.json();
            const recommendationsDiv = document.getElementById('recommendations');
            recommendationsDiv.innerHTML = `
                <h2>Recommendations:</h2>
                <pre>${JSON.stringify(result.recommendations, null, 2)}</pre>
            `;
        } catch (error) {
            console.error('Error:', error);
        }
    });
});

from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "ca6be27f7171af261db33fe5d49fa9fb"

@app.route('/', methods=['GET', 'POST'])
def weather():
    weather_data = None
    error = None
    if request.method == 'POST':
        city = request.form.get('city')
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        print(f"[DEBUG] API Response Code: {response.status_code}")
        print(f"[DEBUG] API Response Body: {response.text}")
        if response.ok:
            data = response.json()
            weather_data = {
                "city": data['name'],
                "temperature": f"{data['main']['temp']} °C",
                "wind": f"{data['wind']['speed']} m/s",
                "description": data['weather'][0]['description'].title()
            }
        else:
            error = f"Error: {response.json().get('message', 'Something went wrong.')}"
    return render_template('index.html', weather=weather_data, error=error)

if __name__ == '__main__':
    app.run(debug=True)

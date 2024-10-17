from flask import Flask, render_template, request, redirect, url_for, flash
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Retrieve the API key from environment variables
API_KEY = os.getenv('API_KEY')

# Ensure the API key is available
if not API_KEY:
    raise Exception("API_KEY is not set in .env file.")

API_URL = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/'

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        base_currency = request.form.get('base_currency').upper()
        target_currency = request.form.get('target_currency').upper()
        amount = float(request.form.get('amount'))

        # Fetch exchange rate data
        response = requests.get(f"{API_URL}{base_currency}")
        if response.status_code == 200:
            data = response.json()
            if 'conversion_rates' in data:
                conversion_rate = data['conversion_rates'].get(target_currency)
                if conversion_rate:
                    converted_amount = amount * conversion_rate
                    return render_template('index.html', result=converted_amount, base=base_currency, target=target_currency, amount=amount)
                else:
                    flash(f"Invalid target currency: {target_currency}")
            else:
                flash(f"Error fetching data for base currency: {base_currency}")
        else:
            flash("API error: Failed to fetch data.")

        return redirect(url_for('home'))

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

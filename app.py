from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

with open('scaler.pkl', 'rb') as file:
    scaler = pickle.load(file)

@app.route('/')
def home():
    return render_template('index.html', prediction=None)

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        administration = float(request.form['administration'])
        marketing_spend = float(request.form['marketing_spend'])
        rd_spend = float(request.form['rd_spend'])
        city = int(request.form['city'])

        scaled_values = scaler.transform([[administration, marketing_spend, rd_spend, city]])
        
        input_data = scaled_values.tolist()[0]
        
        prediction = model.predict([input_data])[0]
        print(prediction)
        
        return render_template('index.html', predictions=prediction)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load the trained model
with open('randomfrsmt.sav', 'rb') as model_file:
    model = pickle.load(model_file)

@app.route('/')
def hello_world():
    return render_template("login.html")

database = {'ranjit':'kulkarni', 'ayush':'shah', 'abhinav':'atram', 'swapnil':'more'}

@app.route('/form_login', methods=['POST'])
def login():
    name1 = request.form['username']
    pwd = request.form['password']
    if name1 not in database:
        return render_template('login.html', info='Invalid User')
    else:
        if database[name1] != pwd:
            return render_template('login.html', info='Invalid Password')
        else:
            return render_template('index.html', name=name1)

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Retrieve input values
    input_values = {key: request.form[key] for key in request.form.keys()}

    # Convert input values to float for prediction
    features = [float(x) for x in request.form.values()]
    features = np.array(features).reshape(1, -1)

    # Predict churn
    prediction = model.predict(features)
    if prediction[0] == 1:
        churn_message = "The customer is likely to churn."
    else:
        churn_message = "The customer is not likely to churn."

    # Map gender values to labels
    gender_label = 'Male' if input_values['Gender'] == '1' else 'Female'

    # Map income category values to labels
    income_category_label = {
        '1': 'Less than $40K',
        '2': '$40K - $60K',
        '3': '$60K - $80K',
        '4': '$80K - $120K',
        '5': '$120K+'
    }.get(input_values['Income_Category'], 'Unknown')

    return render_template('index.html', prediction=prediction[0], churn_message=churn_message,
                           input_values=input_values, gender_label=gender_label,
                           income_category_label=income_category_label)


# Function to map encoded values to their corresponding labels
def map_values_to_labels(input_values):
    gender_label = 'Male' if input_values['Gender'] == '1' else 'Female'
    income_category_label = {
        '1': 'Less than $40K',
        '2': '$40K - $60K',
        '3': '$60K - $80K',
        '4': '$80K - $120K',
        '5': '$120K+'
    }.get(input_values['Income_Category'], 'Unknown')

    return {
        'Customer_Age': input_values['Customer_Age'],
        'Gender': gender_label,
        'Dependent_count': input_values['Dependent_count'],
        'Income_Category': income_category_label,
        'Months_on_book': input_values['Months_on_book'],
        'Credit_Limit': input_values['Credit_Limit'],
        'Total_Trans_Ct': input_values['Total_Trans_Ct'],
        'Total_Trans_Amt': input_values['Total_Trans_Amt']
    }

if __name__ == '__main__':
    app.run(debug=True)

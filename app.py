from flask import Flask, request
import pickle

app = Flask(__name__) # app initialization

#loading the model
model_pickle = open("./artefacts/classifier.pkl", "rb")
clf = pickle.load(model_pickle)

#first endpoint
@app.route("/ping", methods = ['GET'])  #we are mapping our function to a particular endpoint
def ping():
    return {"message" : "Hi there, this endpoint is working!!!!"}


##defining the endpoint for classification
@app.route("/predict", methods = ['Post', 'GET'])
def prediction():
    '''
    Returns the loan application status using ML model.
    '''
    loan_req = request.get_json()
    if loan_req['Gender'] == 'Male':
        Gender = 0
    else:
        Gender = 1

    if loan_req['married'] == 'Unmarried':
        marital_status = 0
    else:
        marital_status = 1

    if loan_req['credit_history'] == 'Unclear Debts':
        credit_status = 0
    else:
        credit_status = 1

    applicant_income = loan_req['applicant_income']
    loan_amt = loan_req['loan_amount']

    result = clf.predict([[Gender, marital_status, applicant_income, loan_amt, credit_status]])

    if result == 0:
        pred = "Rejected"
    else:
        pred = "Approved"

    return {"loan_approval_status" : pred}



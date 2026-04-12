from flask import Flask, render_template, request, jsonify
#'Flask' is th emain calss - it creates your web server
#'render_template' is a function that loads an HTML file from the templates/ folder
#'request' lets Flask reaad data sent from a browser
#'jsonify' converts a python dict into a JSON responsse
from google import genai
import os 
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

#to create the app

app = Flask(__name__)
#this creates flask application 
#__name__ is a built in python variable that tells Flask where your file is located, so __name__ is the path
# Flask uses it to find the templates/ folder relative to this file

#ROUTE 1

@app.route("/")
#this decorator tells flask when someone visits http://localhost:5000/, run the function below
# "/" is the root url - the homepage

def home():
    return render_template("index.html")
    # render_template() loads index.html from the templates/ folder
    # and sends it to the browser as a complete HTML page

#ROUTE 2

@app.route("/ask", methods=["POST"])
#/ask is the url this route responds to
#methods=["POST"] means this route only accepts POST requests
# POST is used when you are sending data to the server, not just visiting a page
# GET is for visiting pages, POST is for sending data

def ask():
    data = request.get_json()
    # request.get_json() reads the JSON data sent from JS 
    # It converts it into a Python dictionary

    message = data["message"]
    #reads the "message" key from the dict
    #this is what the user typed in the input field of the html

    if message == "":
        response_text = "You sent an empty message"
    else:
        try:        #gemini API call
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=message
            )
            response_text = response.text
        except Exception as e:
            response_text = f"There has been an error: {e} "
            

    return jsonify({"response": response_text}) 
    #jsonify converts python dict to JSON response
    #JS on the frontend will read the "response" key from this

#ROUTE 3

@app.route("/ping", methods=["GET"])

def ping(): 
    return jsonify({"status": "server is running"})


#RUN THE SERVER

if __name__ == "__main__":
    app.run(debug=True)

#if __name__ == "__main__" - was for only run this if you execute this file directly
#app.run() - starts the flask server
# debug=True means Flask will auto-reload when you save changes
# and show detailed error messages - only use this in development, never in production





from flask import Flask, render_template, redirect
from flask_pymongo import pymongo
import scrape_mars
# Create an instance of our Flask app.
app = Flask(__name__)

# Create variable for our connection string

conn = 'mongodb://localhost:27017'

# Pass connection string to the pymongo instance.
client = pymongo.MongoClient(conn)
# Connect to a database. 

# If the database doesn't already exist, our code will create it automatically as soon as we insert a record.
db = client.scrape_db
mars_facts = db.mars_facts
#mars_facts.drop()


# Render the index.html page with any craigslist listings in our database. 
# If there are no listings, the table will be empty.
@app.route("/")
def index():
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    mars_results = mars_facts.find_one()
    return render_template("index.html", mars_results=mars_results)

# This route will trigger the webscraping, but it will then send us back to the index route to render the results
@app.route("/scrape")
def scraper():
    # Drops collection if available to remove duplicates
    mars_facts.drop()
    # scrape_mars.scrape() is a custom function that we've defined in the scrape_mars.py file within this directory
    mars_data = scrape_mars.scrape()
    mars_facts.insert_many(mars_data)
    
    # Use Flask's redirect function to send us to a different route once this task has completed.
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)

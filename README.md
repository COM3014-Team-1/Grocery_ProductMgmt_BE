# Grocery_ProductMgmt_BE_MS
This is Product Management Microservice.

Initial setup:

virtual env setup:
run these commands in terminal
    pip install virtualenv
    python -m venv venv

    window: venv\Scripts\activate
    macOS/Linux: source venv/bin/activate

run the following commands:
    pip install -r requirements.txt

create a database in postgres sql and with this name "grocery_Product"

Update the appsettings.development.config (username, password and port) ->"DATABASE_URL" :  "postgresql://username:password@localhost:port/grocery_Product"

Replace this value in the file appsettings.development.config after setting the values accordingly

Run these commands in the terminal:
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade

To run the application
    flask run

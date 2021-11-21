from config import connex_app


# Read the swagger.yml file to configure endpoints
connex_app.add_api("swagger.yml")

import views

# If we're running in stand alone mode, run the application
if __name__ == "__main__":
    connex_app.run(debug=True)

from web import create_app

if __name__ == "__main__":
    """
    This script creates and runs a Flask application.
    """
    app = create_app()
    app.run(debug=True)
from app import app
import config

if __name__ == "__main__":
    app.run(debug=config.Flask_Config.DEBUG, use_reloader=False)

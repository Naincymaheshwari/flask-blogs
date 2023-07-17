from flask_migrate import MigrateCommand
from app import create_app
from flask_script import Manager
from flask_script import Server
import config

hostenv = "default"


app = create_app(hostenv)
manager = Manager(app)
manager.add_command("runserver", Server(host="127.0.0.1", port=config.PORT))
manager.add_command("db", MigrateCommand)


if __name__ == "__main__":
    manager.run()

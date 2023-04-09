import os

from flask import Flask, render_template
# register the database commands
from labcert import db
# apply the blueprints to the app
from labcert import auth, certs


def page_not_found(e):
    return render_template('errors/404.html'), 404


def internal_error(e):
    return render_template('errors/500.html'), 404


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY=os.urandom(12).hex() if not app.debug else "dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "labcert.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance and certificate folder exists
    try:
        app.config["cert_path"] = os.path.join(app.instance_path, "certs")
        os.makedirs(app.config["cert_path"])
    except OSError:
        pass

    db.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(certs.bp)

    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_error)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="index")

    return app

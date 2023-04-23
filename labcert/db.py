import sqlite3
import os
import datetime
import click
from flask import current_app as app
from flask import g
from cryptography import x509
from werkzeug.local import LocalProxy

logger = LocalProxy(lambda: app.logger)


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        g.db = sqlite3.connect(
            app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    """Clear existing data and create new tables."""
    db = get_db()

    with app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


def import_certificate(cert: x509.Certificate):
    pass  # TODO


def load_db():
    """Importing certificate files."""
    cert_folder = app.config["cert_path"]
    for filename in os.listdir(cert_folder):
        with open(os.path.join(cert_folder, filename), "rb") as file:
            cert = x509.load_pem_x509_certificates(file.read())
            import_certificate(cert[0])


def update_status():
    db = get_db()
    certs = db.execute("SELECT * FROM certs").fetchall()
    for cert in certs:
        if cert["cert_status"] == "Valid":
            if cert["cert_not_valid_after"] < datetime.datetime.now():
                db.execute("UPDATE certs SET cert_status = ? WHERE cert_id = ?",
                           ("Expired", cert["cert_id"]))
        elif cert["cert_status"] == "Active":
            if cert["cert_not_valid_before"] >= datetime.datetime.now():
                db.execute("UPDATE certs SET cert_status = ? WHERE cert_id = ?",
                           ("Active", cert["cert_id"]))
    db.commit()


@click.command("init-db")
def init_db_command():
    """Clear existing users and create tables."""
    init_db()
    click.echo("Initialized the database.")
    load_db()
    click.echo("Certificate files imported to database.")


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

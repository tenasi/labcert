from flask import Blueprint
from flask import render_template
from flask import current_app
from flask import request
from flask import flash
from werkzeug.local import LocalProxy

from labcert.auth import login_required
from labcert.db import get_db, init_db, update_status

from cryptography import x509

import os
import datetime
import uuid

bp = Blueprint("certs", __name__, url_prefix="/certs")
logger = LocalProxy(lambda: current_app.logger)


class settings:
    def __init__(self, show_issuer) -> None:
        self.show_issuer = show_issuer


@bp.route("/samples")
@login_required
def samples():
    db = get_db()
    db.execute(
        "INSERT INTO certs (cert_name, cert_level, cert_type,\
        cert_status, cert_serial, cert_not_valid_before, cert_not_valid_after,\
        subject_name, subject_algorithm, subject_strength)\
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            "Tenasi Root",
            1,
            "Root CA",
            "Valid",
            "TBD",
            datetime.datetime.now(),
            datetime.datetime.now(),
            "C = de, ST = Bavaria, L = Munich, O = Tenasi, OU = Admin, CN = tenasi, emailAddress = jip@tenasi.de",
            "RSA",
            "4096",
        ),
    )
    db.execute(
        "INSERT INTO certs (cert_name, cert_level, cert_type,\
        cert_status, cert_serial, cert_not_valid_before, cert_not_valid_after,\
        subject_name, subject_algorithm, subject_strength, issuer_id, issuer_name,\
        issuer_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            "Tenasi Intermediate",
            2,
            "Intermediate",
            "Valid",
            "TBD",
            datetime.datetime.now(),
            datetime.datetime.now(),
            "tenasi",
            "RSA",
            "4096",
            1,
            "Tenasi Root",
            "Root CA",
        ),
    )
    db.execute(
        "INSERT INTO certs (cert_name, cert_level, cert_type,\
        cert_status, cert_serial, cert_not_valid_before, cert_not_valid_after,\
        subject_name, subject_algorithm, subject_strength, issuer_id, issuer_name,\
        issuer_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            "Unifi",
            3,
            "End Entity",
            "Valid",
            "TBD",
            datetime.datetime.now(),
            datetime.datetime.now(),
            "unifi",
            "RSA",
            "4096",
            2,
            "Tenasi Intermediate",
            "Intermediate",
        ),
    )
    db.execute(
        "INSERT INTO certs (cert_name, cert_level, cert_type,\
        cert_status, cert_serial, cert_not_valid_before, cert_not_valid_after,\
        subject_name, subject_algorithm, subject_strength, issuer_id, issuer_name,\
        issuer_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            "Optimus",
            3,
            "End Entity",
            "Valid",
            "TBD",
            datetime.datetime.now(),
            datetime.datetime.now(),
            "unifi",
            "RSA",
            "4096",
            2,
            "Tenasi Intermediate",
            "Intermediate",
        ),
    )
    db.execute(
        "INSERT INTO certs (cert_name, cert_level, cert_type,\
        cert_status, cert_serial, cert_not_valid_before, cert_not_valid_after,\
        subject_name, subject_algorithm, subject_strength, issuer_id, issuer_name,\
        issuer_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            "LabCert",
            3,
            "End Entity",
            "Valid",
            "TBD",
            datetime.datetime.now(),
            datetime.datetime.now(),
            "unifi",
            "RSA",
            "4096",
            2,
            "Tenasi Intermediate",
            "Intermediate",
        ),
    )
    db.commit()
    certs = db.execute("SELECT * FROM certs").fetchall()
    update_status()
    return "Done."


@bp.route("/")
@login_required
def index():
    update_status()
    db = get_db()
    certs = db.execute("SELECT * FROM certs").fetchall()
    return render_template("certs/index.html", certs=certs)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    update_status()
    db = get_db()
    issuers = db.execute(
        "SELECT * FROM certs \
        WHERE (cert_type = 'Root CA' OR cert_type = 'Intermediate') \
        AND (cert_status = 'Active' OR cert_status = 'Valid')"
    ).fetchall()

    if request.method == "POST":
        db = get_db()
        # cert_name = request.form["cert_name"]
        # if cert_name:
        #     db.execute(
        #         "UPDATE certs SET cert_name = ? WHERE cert_id = ?", (cert_name, id)
        #     )
        #     db.commit()
        # else:
        #     flash("Certificate Name cannot be empty.")
    return render_template("certs/create.html", issuers=issuers)


@bp.route("/<int:id>", methods=("GET", "POST"))
@login_required
def show(id):
    db = get_db()
    if request.method == "POST":
        cert_name = request.form["cert_name"]
        if cert_name:
            db.execute(
                "UPDATE certs SET cert_name = ? WHERE cert_id = ?", (cert_name, id)
            )
            db.commit()
        else:
            flash("Certificate Name cannot be empty.")
    cert = db.execute("SELECT * FROM certs WHERE cert_id = ?", (id,)).fetchone()
    hierarchy = list()
    hierarchy.append(cert)
    issuer = cert
    while issuer["issuer_id"]:
        issuer_id = issuer["issuer_id"]
        issuer = db.execute(
            "SELECT * FROM certs WHERE cert_id = ?", (issuer_id,)
        ).fetchone()
        hierarchy.insert(0, issuer)

    return render_template("certs/show.html", cert=cert, hierarchy=hierarchy)


# @bp.route("/create_ca", methods=("GET", "POST"))
# @login_required
def gen_root_ca():
    pass


# @bp.route("/create", methods=("GET", "POST"))
# @login_required
def gen_certificate():
    pass


# @bp.route("/certs/exports/<cert>")
# @login_required
def export_cert(cert):
    pass


def check_access(p):
    os.makedirs(p)
    if not os.access(p, os.W_OK):
        logger.error(f"Folder is not writable, check permissions: {p}")
        quit()


def create_path(p):
    if not os.path.exists(p):
        try:
            check_access(p)
        except OSError as e:
            logger.error(f"Error occured while creating path: {p}")
            logger.exception(e)
            quit()


def gen_serial():
    # FIXME
    # serials = list()
    # for file in os.listdir(crt_path):
    #     cert = os.path.join(crt_path, file)
    #     if file == "root.cer":
    #         continue
    #     serial = shell(f"openssl x509 -noout -serial -in {cert}")
    #     serials.append(serial.replace("serial=",""))
    # serial = shell("openssl rand -hex 8")
    # while serial in serials:
    #     serial = shell("openssl rand -hex 8")
    # serial = shell("openssl rand -hex 8")
    # return f"0x{serial}"
    pass

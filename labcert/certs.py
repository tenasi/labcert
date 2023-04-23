from flask import Blueprint
from flask import render_template
from flask import current_app
from werkzeug.local import LocalProxy

from labcert.auth import login_required
from labcert.db import get_db, init_db, update_status

from cryptography import x509

import os
import datetime
import uuid

bp = Blueprint("certs", __name__, url_prefix="/certs")
logger = LocalProxy(lambda: current_app.logger)


class certest:
    def __init__(self, id, name, issuer_id, issuer_name, level, category, status) -> None:
        self.id = id
        self.name = name
        self.level = level
        self.issuer_id = issuer_id
        self.issuer_name = issuer_name
        self.category = category
        self.start_date = datetime.date(2010, 5, 24)
        self.end_date = datetime.date(2010, 5, 24)
        self.status = status


class settings:
    def __init__(self, show_issuer) -> None:
        self.show_issuer = show_issuer


@bp.route("/samples")
@login_required
def samples():
    db = get_db()
    init_db()
    db.execute("INSERT INTO certs (cert_name, cert_level, cert_category,\
        cert_status, cert_serial, cert_not_valid_before, cert_not_valid_after,\
        subject_cn, subject_algorithm, subject_strength)\
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
        "Tenasi Root", 1, "Root CA", "Valid", "TBD", datetime.datetime.now(),
        datetime.datetime.now(), "tenasi", "RSA", "4096"
    ),)
    db.execute("INSERT INTO certs (cert_name, cert_level, cert_category,\
        cert_status, cert_serial, cert_not_valid_before, cert_not_valid_after,\
        subject_cn, subject_algorithm, subject_strength, issuer_id, issuer_name)\
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
        "Tenasi Intermediate", 2, "Intermediate", "Valid", "TBD", datetime.datetime.now(),
        datetime.datetime.now(), "tenasi", "RSA", "4096", 1, "Tenasi Root"
    ),)
    db.execute("INSERT INTO certs (cert_name, cert_level, cert_category,\
        cert_status, cert_serial, cert_not_valid_before, cert_not_valid_after,\
        subject_cn, subject_algorithm, subject_strength, issuer_id, issuer_name)\
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
        "Unifi", 3, "End Entity", "Valid", "TBD", datetime.datetime.now(),
        datetime.datetime.now(), "unifi", "RSA", "4096", 2, "Tenasi Intermediate"
    ),)
    db.execute("INSERT INTO certs (cert_name, cert_level, cert_category,\
        cert_status, cert_serial, cert_not_valid_before, cert_not_valid_after,\
        subject_cn, subject_algorithm, subject_strength, issuer_id, issuer_name)\
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
        "Optimus", 3, "End Entity", "Valid", "TBD", datetime.datetime.now(),
        datetime.datetime.now(), "unifi", "RSA", "4096", 2, "Tenasi Intermediate"
    ),)
    db.execute("INSERT INTO certs (cert_name, cert_level, cert_category,\
        cert_status, cert_serial, cert_not_valid_before, cert_not_valid_after,\
        subject_cn, subject_algorithm, subject_strength, issuer_id, issuer_name)\
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
        "LabCert", 3, "End Entity", "Valid", "TBD", datetime.datetime.now(),
        datetime.datetime.now(), "unifi", "RSA", "4096", 2, "Tenasi Intermediate"
    ),)
    db.commit()
    certs = db.execute(
        "SELECT * FROM certs"
    ).fetchall()
    update_status()
    print(len(certs))
    return "Done."


@bp.route("/test")
@login_required
def test():
    db = get_db()
    certs = db.execute("SELECT * FROM certs").fetchall()
    # certs = [
    #     certest(1, "Tenasi Root", None, "-", 1, "Root CA", "Valid"),
    #     certest(2, "Tenasi Intermediate", 1, "Tenasi Root", 2, "Intermediate", "Error"),
    #     certest(3, "Unifi", 2, "Tenasi Intermediate", 3, "End Entity", "Revoked"),
    #     certest(4, "Optimus", 2, "Tenasi Intermediate", 3, "End Entity", "Revoked"),
    #     certest(5, "LabCert", 2, "Tenasi Intermediate", 3, "End Entity", "Revoked"),
    #     certest(6, "Tenasi Shelly", 1, "Tenasi Root", 2, "Intermediate", "Valid"),
    #     certest(7, "Shelly Hallway Top Right", 6, "Tenasi Shelly", 3, "End Entity", "Valid"),
    #     certest(8, "Shelly Hallway Top Left", 6, "Tenasi Shelly", 3, "End Entity", "Valid"),
    #     certest(9, "Shelly Hallway Bottom Right", 6, "Tenasi Shelly", 3, "End Entity", "Valid"),
    #     certest(1, "Tenasi Root", None, "-", 1, "Root CA", "Valid"),
    #     certest(2, "Tenasi Intermediate", 1, "Tenasi Root", 2, "Intermediate", "Error"),
    #     certest(3, "Unifi", 2, "Tenasi Intermediate", 3, "End Entity", "Revoked"),
    #     certest(4, "Optimus", 2, "Tenasi Intermediate", 3, "End Entity", "Revoked"),
    #     certest(5, "LabCert", 2, "Tenasi Intermediate", 3, "End Entity", "Revoked"),
    #     certest(6, "Tenasi Shelly", 1, "Tenasi Root", 2, "Intermediate", "Valid"),
    #     certest(7, "Shelly Hallway Top Right", 6, "Tenasi Shelly", 3, "End Entity", "Valid"),
    #     certest(8, "Shelly Hallway Top Left", 6, "Tenasi Shelly", 3, "End Entity", "Valid"),
    #     certest(9, "Shelly Hallway Bottom Right", 6, "Tenasi Shelly", 3, "End Entity", "Valid"),
    #     certest(10, "Shelly Hallway Bottom Left", 6, "Tenasi Shelly", 3, "End Entity", "Valid"),
    #     certest(11, "Shelly Bedroom Top", 6, "Tenasi Shelly", 3, "End Entity", "Valid"),
    #     certest(12, "Shelly Bedroom Bottom", 6, "Tenasi Shelly", 3, "End Entity", "Valid"),
    #     certest(13, "Shelly Bathroom", 6, "Tenasi Shelly", 3, "End Entity", "Valid"),
    #     certest(14, "Shelly Guest Toilet", 6, "Tenasi Shelly", 3, "End Entity", "Valid"),
    #     certest(15, "Shelly Kitchen Bar", 6, "Tenasi Shelly", 3, "End Entity", "Valid"),
    #     certest(16, "Shelly Kitchen Cooking", 6, "Tenasi Shelly", 3, "End Entity", "Valid"),
    #     certest(17, "Shelly Living Room Top", 6, "Tenasi Shelly", 3, "End Entity", "Valid"),
    #     certest(18, "Shelly Living Room Middle", 6, "Tenasi Shelly", 3, "End Entity", "Valid"),
    #     certest(19, "Shelly Living Room Bottom", 6, "Tenasi Shelly", 3, "End Entity", "Valid"),
    #     certest(20, "Shelly Server Room", 6, "Tenasi Shelly", 3, "End Entity", "Valid"),
    #     certest(21, "Shelly Entrance", 6, "Tenasi Shelly", 3, "End Entity", "Valid"),
    #     certest(22, "Shelly Power Main", 6, "Tenasi Shelly", 3, "End Entity", "Valid"),
    #     certest(23, "Shelly Power F3", 6, "Tenasi Shelly", 3, "End Entity", "Valid"),
    #     certest(24, "Shelly Power F4", 6, "Tenasi Shelly", 3, "End Entity", "Valid"),
    #     certest(25, "Shelly Power F5", 6, "Tenasi Shelly", 3, "End Entity", "Valid"),
    #     certest(26, "Shelly Power F6", 6, "Tenasi Shelly", 3, "End Entity", "Valid"),
    #     certest(27, "Shelly Power F7", 6, "Tenasi Shelly", 3, "End Entity", "Valid"),
    #     certest(28, "Pihole", 2, "Tenasi Intermediate", 3, "End Entity", "Expired"),
    #     certest(29, "Adguard", 2, "Tenasi Intermediate", 3, "End Entity", "Expired"),
    #     certest(30, "Home Assistant", 2, "Tenasi Intermediate", 3, "End Entity", "Valid"),
    #     certest(31, "Plex", 2, "Tenasi Intermediate", 3, "End Entity", "Valid"),
    #     certest(32, "Mastodon", 2, "Tenasi Intermediate", 3, "End Entity", "Valid"),
    #     certest(33, "Wiki", 2, "Tenasi Intermediate", 3, "End Entity", "Valid"),
    #     certest(34, "Database", 2, "Tenasi Intermediate", 3, "End Entity", "Valid"),
    #     certest(35, "Web", 2, "Tenasi Intermediate", 3, "End Entity", "Valid"),
    #     certest(36, "Oktoprint", 2, "Tenasi Intermediate", 3, "End Entity", "Valid"),
    #     certest(31, "Plex", 2, "Tenasi Intermediate", 4, "End Entity", "Valid"),
    #     certest(32, "Mastodon", 2, "Tenasi Intermediate", 4, "End Entity", "Valid"),
    #     certest(33, "Wiki", 2, "Tenasi Intermediate", 4, "End Entity", "Valid"),
    #     certest(34, "Database", 2, "Tenasi Intermediate", 4, "End Entity", "Valid"),
    #     certest(35, "Web", 2, "Tenasi Intermediate", 4, "End Entity", "Valid"),
    #     certest(36, "Oktoprint", 2, "Tenasi Intermediate", 4, "End Entity", "Valid"),
    #     certest(2, "Tenasi Intermediate", 1, "Tenasi Root", 2, "Intermediate", "Error"),
    #     certest(3, "Unifi", 2, "Tenasi Intermediate", 3, "End Entity", "Revoked"),
    #     certest(4, "Optimus", 2, "Tenasi Intermediate", 3, "End Entity", "Revoked"),
    #     certest(5, "LabCert", 2, "Tenasi Intermediate", 3, "End Entity", "Revoked"),
    #     certest(6, "Tenasi Shelly", 1, "Tenasi Root", 2, "Intermediate", "Valid"),
    #     certest(7, "Shelly Hallway Top Right", 6, "Tenasi Shelly", 3, "End Entity", "Valid"),
    #     certest(8, "Shelly Hallway Top Left", 6, "Tenasi Shelly", 3, "End Entity", "Valid"),
    #     certest(9, "Shelly Hallway Bottom Right", 6, "Tenasi Shelly", 3, "End Entity", "Valid"),
    # ]
    # s = settings(True)
    # empty_fields = range(max(0, 10-len(certs)))
    return render_template("test.html", certs=certs)


@bp.route("/test2")
def test2():
    return render_template("test2.html")


@bp.route("/")
def index():
    db = get_db()
    certs = db.execute("SELECT * FROM certs").fetchall()
    return render_template("certs/index.html", certs=certs)


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

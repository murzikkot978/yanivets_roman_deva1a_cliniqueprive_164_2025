"""Gestion des "routes" FLASK et des données pour les medecin.
Fichier : gestion_genres_crud.py
Auteur : OM 2021.03.16
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for
from flask import render_template, flash
from wtforms import HiddenField, SelectField, DateField
from wtforms.validators import InputRequired, DataRequired

from APP_FILMS_164 import app
from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *
from APP_FILMS_164.consultations.gestion_consultations_wtf_forms import FormWTFAjouterConsultations
from APP_FILMS_164.consultations.gestion_consultations_wtf_forms import FormWTFDeleteConsultation
from APP_FILMS_164.consultations.gestion_consultations_wtf_forms import FormWTFUpdateConsultation

FormWTFAjouterConsultations.id_consultation_hidden = HiddenField()
FormWTFUpdateConsultation.id_consultation_hidden = HiddenField()

@app.route("/consultations_afficher/<string:order_by>/<int:id_consultation_sel>", methods=['GET', 'POST'])
def consultations_afficher(order_by, id_consultation_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_consultation_sel == 0:
                    strsql = """
                        SELECT c.id_consultation, c.date_consultation,
                               m.nom_medecin, p.nom_pationt
                        FROM t_consultation c
                        LEFT JOIN t_medecin m ON c.fk_medecin = m.id_medecin
                        LEFT JOIN t_pationt p ON c.fk_pationt = p.id_pationt
                    """
                    mc_afficher.execute(strsql)
                elif order_by == "ASC":
                    strsql = """
                        SELECT c.id_consultation, c.date_consultation,
                               m.nom_medecin, p.nom_pationt
                        FROM t_consultation c
                        LEFT JOIN t_medecin m ON c.fk_medecin = m.id_medecin
                        LEFT JOIN t_pationt p ON c.fk_pationt = p.id_pationt
                        WHERE c.id_consultation = %(value_id_consultation_selected)s
                    """
                    mc_afficher.execute(strsql, {"value_id_consultation_selected": id_consultation_sel})
                else:
                    strsql = """
                        SELECT c.id_consultation, c.date_consultation,
                               m.nom_medecin, p.nom_pationt
                        FROM t_consultation c
                        LEFT JOIN t_medecin m ON c.fk_medecin = m.id_medecin
                        LEFT JOIN t_pationt p ON c.fk_pationt = p.id_pationt
                    """
                    mc_afficher.execute(strsql)
                data_consultations = mc_afficher.fetchall()
                if not data_consultations and id_consultation_sel == 0:
                    flash("""La table "t_consultation" est vide. !!""", "warning")
                elif not data_consultations and id_consultation_sel > 0:
                    flash(f"La consultation demandée n'existe pas !!", "warning")
                else:
                    flash(f"Données consultations affichées !!", "success")
        except Exception as Exception_consultations_afficher:
            raise ExceptionGenresAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{consultations_afficher.__name__} ; "
                                          f"{Exception_consultations_afficher}")
    return render_template("consultation/consultations_afficher.html", data=data_consultations)

@app.route("/consultation_ajouter_wtf", methods=['GET', 'POST'])
def consultation_ajouter_wtf():
    form = FormWTFAjouterConsultations()
    # Fetch medecins and patients for select fields
    with DBconnection() as mconn_bd:
        mconn_bd.execute("SELECT id_medecin, nom_medecin FROM t_medecin")
        medecins = mconn_bd.fetchall()
        mconn_bd.execute("SELECT id_pationt, nom_pationt FROM t_pationt")
        patients = mconn_bd.fetchall()
    # Set choices for SelectFields
    form.fk_medecin.choices = [(row["id_medecin"], row["nom_medecin"]) for row in medecins]
    form.fk_patient.choices = [(row["id_pationt"], row["nom_pationt"]) for row in patients]

    if request.method == "POST":
        try:
            if form.validate_on_submit():
                fk_medecin = form.fk_medecin.data
                fk_patient = form.fk_patient.data
                date_consultation = form.date_consultation.data

                valeurs_insertion = {
                    "value_fk_medecin": fk_medecin,
                    "value_fk_patient": fk_patient,
                    "value_date_consultation": date_consultation
                }
                strsql_insert = """
                    INSERT INTO t_consultation (fk_medecin, fk_pationt, date_consultation)
                    VALUES (%(value_fk_medecin)s, %(value_fk_patient)s, %(value_date_consultation)s)
                """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert, valeurs_insertion)

                flash("Консультация успешно добавлена!", "success")
                return redirect(url_for('consultations_afficher', order_by='ASC', id_consultation_sel=0))
        except Exception as e:
            raise ExceptionGenresAjouterWtf(f"Ошибка при добавлении consultation : {e}")

    return render_template("consultation/consultations_ajouter_wtf.html", form=form)

@app.route("/consultation_update_wtf", methods=['GET', 'POST'])
def consultation_update_wtf():
    form = FormWTFUpdateConsultation()
    # Fetch medecins and patients for select fields
    with DBconnection() as mconn_bd:
        mconn_bd.execute("SELECT id_medecin, nom_medecin FROM t_medecin")
        medecins = mconn_bd.fetchall()
        mconn_bd.execute("SELECT id_pationt, nom_pationt FROM t_pationt")
        patients = mconn_bd.fetchall()
    form.fk_medecin.choices = [(row["id_medecin"], row["nom_medecin"]) for row in medecins]
    form.fk_patient.choices = [(row["id_pationt"], row["nom_pationt"]) for row in patients]

    if request.method == "POST":
        id_consultation_update = form.id_consultation_hidden.data
    else:
        id_consultation_update = request.values.get('id_consultation_btn_edit_html')

    if request.method == "POST" and form.validate_on_submit():
        try:
            fk_medecin = form.fk_medecin.data
            fk_patient = form.fk_patient.data
            date_consultation = form.date_consultation.data

            valeurs_update = {
                "value_id_consultation": id_consultation_update,
                "value_fk_medecin": fk_medecin,
                "value_fk_patient": fk_patient,
                "value_date_consultation": date_consultation
            }
            strsql_update = """
                UPDATE t_consultation
                SET fk_medecin = %(value_fk_medecin)s,
                    fk_pationt = %(value_fk_patient)s,
                    date_consultation = %(value_date_consultation)s
                WHERE id_consultation = %(value_id_consultation)s
            """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(strsql_update, valeurs_update)

            flash("Данные консультации успешно обновлены!", "success")
            return redirect(url_for('consultations_afficher', order_by='ASC', id_consultation_sel=0))
        except Exception as e:
            raise ExceptionGenresAjouterWtf(f"Ошибка при обновлении consultation : {e}")

    elif request.method == "GET":
        strsql_select = "SELECT * FROM t_consultation WHERE id_consultation = %(value_id_consultation)s"
        with DBconnection() as mconn_bd:
            mconn_bd.execute(strsql_select, {"value_id_consultation": id_consultation_update})
            data_consultation = mconn_bd.fetchone()
            if data_consultation:
                form.id_consultation_hidden.data = data_consultation["id_consultation"]
                form.fk_medecin.data = data_consultation["fk_medecin"]
                form.fk_patient.data = data_consultation["fk_pationt"]
                form.date_consultation.data = data_consultation["date_consultation"]

    return render_template("consultation/consultation_update_wtf.html", form_update=form)

@app.route("/consultation_delete_wtf", methods=['GET', 'POST'])
def consultation_delete_wtf():
    id_consultation_delete = request.values.get('id_consultation_btn_delete_html')
    form_delete = FormWTFDeleteConsultation()
    consultation_info = ""
    if request.method == "POST" and form_delete.validate_on_submit():
        if form_delete.submit_btn_annuler.data:
            return redirect(url_for("consultations_afficher", order_by="ASC", id_consultation_sel=0))
        if form_delete.submit_btn_conf_del.data:
            return render_template("consultation/consultation_delete_wtf.html", form_delete=form_delete, btn_submit_del=True, consultation_info=consultation_info)
        if form_delete.submit_btn_del.data:
            try:
                strsql_delete = "DELETE FROM t_consultation WHERE id_consultation = %(value_id_consultation)s"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_delete, {"value_id_consultation": id_consultation_delete})
                flash("Консультация успешно удалена!", "success")
                return redirect(url_for('consultations_afficher', order_by="ASC", id_consultation_sel=0))
            except Exception as e:
                raise ExceptionGenresAjouterWtf(f"Ошибка при удалении consultation : {e}")

    elif request.method == "GET":
        strsql_select = "SELECT * FROM t_consultation WHERE id_consultation = %(value_id_consultation)s"
        with DBconnection() as mconn_bd:
            mconn_bd.execute(strsql_select, {"value_id_consultation": id_consultation_delete})
            data_consultation = mconn_bd.fetchone()
            if data_consultation:
                consultation_info = f"ID: {data_consultation['id_consultation']}, Врач: {data_consultation['fk_medecin']}, Пациент: {data_consultation['fk_pationt']}, Дата: {data_consultation['date_consultation']}"
                form_delete.nom_genre_delete_wtf.data = consultation_info

    return render_template("consultation/consultation_delete_wtf.html", form_delete=form_delete, btn_submit_del=False, consultation_info=consultation_info, data_films_associes=None)

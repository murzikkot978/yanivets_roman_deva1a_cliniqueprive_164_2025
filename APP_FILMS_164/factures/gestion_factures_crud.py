"""Gestion des "routes" FLASK et des données pour les medecin.
Fichier : gestion_facture_crud.py
Auteur : OM 2021.03.16
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for
from flask import render_template, flash  # already imported
from wtforms import HiddenField, SelectField, IntegerField, DateField
from wtforms.validators import InputRequired, DataRequired, NumberRange

from APP_FILMS_164 import app
from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *
from APP_FILMS_164.factures.gestion_factures_wtf_forms import FormWTFAjouterFactures
from APP_FILMS_164.factures.gestion_factures_wtf_forms import FormWTFDeleteFacture
from APP_FILMS_164.factures.gestion_factures_wtf_forms import FormWTFUpdateFacture

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /facture_afficher
    
    Test : ex : http://127.0.0.1:5575/facture_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_genre_sel = 0 >> tous les medecin.
                id_genre_sel = "n" affiche le genre dont l'id est "n"
"""


@app.route("/facture_afficher/<string:order_by>/<int:id_facture_sel>", methods=['GET', 'POST'])
def facture_afficher(order_by, id_facture_sel):
    return factures_afficher(order_by, id_facture_sel)


@app.route("/factures_afficher/<string:order_by>/<int:id_facture_sel>", methods=['GET', 'POST'])
def factures_afficher(order_by, id_facture_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_facture_sel == 0:
                    strsql = """
                        SELECT f.id_facture, f.montant, f.date_emission, f.fk_consultation, f.fk_pationt,
                               p.nom_pationt, c.date_consultation
                        FROM t_facture f
                        LEFT JOIN t_pationt p ON f.fk_pationt = p.id_pationt
                        LEFT JOIN t_consultation c ON f.fk_consultation = c.id_consultation
                    """
                    mc_afficher.execute(strsql)
                elif order_by == "ASC":
                    strsql = """
                        SELECT f.id_facture, f.montant, f.date_emission, f.fk_consultation, f.fk_pationt,
                               p.nom_pationt, c.date_consultation
                        FROM t_facture f
                        LEFT JOIN t_pationt p ON f.fk_pationt = p.id_pationt
                        LEFT JOIN t_consultation c ON f.fk_consultation = c.id_consultation
                        WHERE f.id_facture = %(value_id_facture_selected)s
                    """
                    mc_afficher.execute(strsql, {"value_id_facture_selected": id_facture_sel})
                else:
                    strsql = """
                        SELECT f.id_facture, f.montant, f.date_emission, f.fk_consultation, f.fk_pationt,
                               p.nom_pationt, c.date_consultation
                        FROM t_facture f
                        LEFT JOIN t_pationt p ON f.fk_pationt = p.id_pationt
                        LEFT JOIN t_consultation c ON f.fk_consultation = c.id_consultation
                    """
                    mc_afficher.execute(strsql)
                data_facture = mc_afficher.fetchall()
                if not data_facture and id_facture_sel == 0:
                    flash("""La table "t_facture" est vide. !!""", "warning")
                elif not data_facture and id_facture_sel > 0:
                    flash(f"La facture demandée n'existe pas !!", "warning")
                else:
                    flash(f"Données factures affichées !!", "success")
        except Exception as Exception_facture_afficher:
            raise ExceptionFacturesAfficher(f"fichier : {Path(__file__).name}  ;  "
                                            f"{factures_afficher.__name__} ; "
                                            f"{Exception_facture_afficher}")
    return render_template("facture/factures_afficher.html", data=data_facture)


@app.route("/facture_ajouter_wtf", methods=['GET', 'POST'])
@app.route("/factures_ajouter_wtf", methods=['GET', 'POST'])
def facture_ajouter_wtf():
    form = FormWTFAjouterFactures()
    # Fetch patients and consultations for select fields
    with DBconnection() as mconn_bd:
        mconn_bd.execute("SELECT id_pationt, nom_pationt FROM t_pationt")
        patients = mconn_bd.fetchall()
        mconn_bd.execute("SELECT id_consultation, date_consultation FROM t_consultation")
        consultations = mconn_bd.fetchall()
    form.fk_pationt.choices = [(row["id_pationt"], row["nom_pationt"]) for row in patients]
    form.fk_consultation.choices = [(row["id_consultation"], str(row["date_consultation"])) for row in consultations]

    if request.method == "POST":
        try:
            if form.validate_on_submit():
                fk_pationt = form.fk_pationt.data
                montant = form.montant.data
                date_emission = form.date_emission.data
                fk_consultation = form.fk_consultation.data

                valeurs_insertion = {
                    "value_fk_pationt": fk_pationt,
                    "value_montant": montant,
                    "value_date_emission": date_emission,
                    "value_fk_consultation": fk_consultation
                }
                strsql_insert = """
                    INSERT INTO t_facture (fk_pationt, montant, date_emission, fk_consultation)
                    VALUES (%(value_fk_pationt)s, %(value_montant)s, %(value_date_emission)s, %(value_fk_consultation)s)
                """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert, valeurs_insertion)

                flash("Фактура успешно добавлена!", "success")
                return redirect(url_for('facture_afficher', order_by='ASC', id_facture_sel=0))
        except Exception as e:
            raise ExceptionFacturesAjouterWtf(f"Ошибка при добавлении facture : {e}")

    return render_template("facture/factures_ajouter_wtf.html", form=form)


@app.route("/facture_update_wtf", methods=['GET', 'POST'])
def facture_update_wtf():
    form = FormWTFUpdateFacture()
    with DBconnection() as mconn_bd:
        mconn_bd.execute("SELECT id_pationt, nom_pationt FROM t_pationt")
        patients = mconn_bd.fetchall()
        mconn_bd.execute("SELECT id_consultation, date_consultation FROM t_consultation")
        consultations = mconn_bd.fetchall()
    form.fk_pationt.choices = [(row["id_pationt"], row["nom_pationt"]) for row in patients]
    form.fk_consultation.choices = [(row["id_consultation"], str(row["date_consultation"])) for row in consultations]

    if request.method == "POST":
        id_facture_update = form.id_facture_hidden.data
    else:
        id_facture_update = request.values.get('id_facture_btn_edit_html')

    if request.method == "POST" and form.validate_on_submit():
        try:
            fk_pationt = form.fk_pationt.data
            montant = form.montant.data
            date_emission = form.date_emission.data
            fk_consultation = form.fk_consultation.data

            valeurs_update = {
                "value_id_facture": id_facture_update,
                "value_fk_pationt": fk_pationt,
                "value_montant": montant,
                "value_date_emission": date_emission,
                "value_fk_consultation": fk_consultation
            }
            strsql_update = """
                UPDATE t_facture
                SET fk_pationt = %(value_fk_pationt)s,
                    montant = %(value_montant)s,
                    date_emission = %(value_date_emission)s,
                    fk_consultation = %(value_fk_consultation)s
                WHERE id_facture = %(value_id_facture)s
            """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(strsql_update, valeurs_update)

            flash("Данные фактуры успешно обновлены!", "success")
            return redirect(url_for('facture_afficher', order_by='ASC', id_facture_sel=0))
        except Exception as e:
            raise ExceptionFacturesAjouterWtf(f"Ошибка при обновлении facture : {e}")

    elif request.method == "GET":
        strsql_select = "SELECT * FROM t_facture WHERE id_facture = %(value_id_facture)s"
        with DBconnection() as mconn_bd:
            mconn_bd.execute(strsql_select, {"value_id_facture": id_facture_update})
            data_facture = mconn_bd.fetchone()
            if data_facture:
                form.id_facture_hidden.data = data_facture["id_facture"]
                form.fk_pationt.data = data_facture["fk_pationt"]
                form.montant.data = data_facture["montant"]
                form.date_emission.data = data_facture["date_emission"]
                form.fk_consultation.data = data_facture["fk_consultation"]

    return render_template("facture/facture_update_wtf.html", form_update=form)


@app.route("/facture_delete_wtf", methods=['GET', 'POST'])
def facture_delete_wtf():
    id_facture_delete = request.values.get('id_facture_btn_delete_html')
    form_delete = FormWTFDeleteFacture()
    facture_info = ""
    if request.method == "POST" and form_delete.validate_on_submit():
        if form_delete.submit_btn_annuler.data:
            return redirect(url_for("facture_afficher", order_by="ASC", id_facture_sel=0))
        if form_delete.submit_btn_conf_del.data:
            return render_template("facture/facture_delete_wtf.html", form_delete=form_delete, btn_submit_del=True, facture_info=facture_info)
        if form_delete.submit_btn_del.data:
            try:
                strsql_delete = "DELETE FROM t_facture WHERE id_facture = %(value_id_facture)s"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_delete, {"value_id_facture": id_facture_delete})
                flash("Фактура успешно удалена!", "success")
                return redirect(url_for('facture_afficher', order_by="ASC", id_facture_sel=0))
            except Exception as e:
                raise ExceptionFacturesAjouterWtf(f"Ошибка при удалении facture : {e}")

    elif request.method == "GET":
        strsql_select = "SELECT * FROM t_facture WHERE id_facture = %(value_id_facture)s"
        with DBconnection() as mconn_bd:
            mconn_bd.execute(strsql_select, {"value_id_facture": id_facture_delete})
            data_facture = mconn_bd.fetchone()
            if data_facture:
                facture_info = f"ID: {data_facture['id_facture']}, Пациент: {data_facture['fk_pationt']}, Сумма: {data_facture['montant']}, Дата: {data_facture['date_emission']}, Консультация: {data_facture['fk_consultation']}"
                form_delete.nom_genre_delete_wtf.data = facture_info

    return render_template("facture/facture_delete_wtf.html", form_delete=form_delete, btn_submit_del=False, facture_info=facture_info, data_films_associes=None)

"""Gestion des "routes" FLASK et des données pour les specialite.
Fichier : gestion_specialites_crud.py
Auteur : OM 2021.03.16
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_FILMS_164 import app
from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *
from APP_FILMS_164.specialites.gestion_specialites_wtf_forms import FormWTFAjouterSpecialites
from APP_FILMS_164.specialites.gestion_specialites_wtf_forms import FormWTFDeleteSpecialite
from APP_FILMS_164.specialites.gestion_specialites_wtf_forms import FormWTFUpdateSpecialite
from wtforms import HiddenField

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /specialites_afficher
    
    Test : ex : http://127.0.0.1:5575/specialites_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_specialite_sel = 0 >> tous les specialites.
                id_specialite_sel = "n" affiche le specialite dont l'id est "n"
"""


@app.route("/specialites_afficher/<string:order_by>/<int:id_specialite_sel>", methods=['GET', 'POST'])
def specialites_afficher(order_by, id_specialite_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_specialite_sel == 0:
                    strsql_specialites_afficher = """SELECT * FROM t_specialite"""
                    mc_afficher.execute(strsql_specialites_afficher)
                elif order_by == "ASC":
                    valeur_id_specialite_selected_dictionnaire = {"value_id_specialite_selected": id_specialite_sel}
                    strsql_specialites_afficher = """SELECT * FROM t_specialite WHERE id_specialite = %(value_id_specialite_selected)s"""
                    mc_afficher.execute(strsql_specialites_afficher, valeur_id_specialite_selected_dictionnaire)
                else:
                    strsql_specialites_afficher = """SELECT * FROM t_specialite"""
                    mc_afficher.execute(strsql_specialites_afficher)

                data_specialites = mc_afficher.fetchall()

                print("data_genres ", data_specialites, " Type : ", type(data_specialites))

                # Différencier les messages si la table est vide.
                if not data_specialites and id_specialite_sel == 0:
                    flash("""La table "t_specialite" est vide. !!""", "warning")
                elif not data_specialites and id_specialite_sel > 0:
                    # Si l'utilisateur change l'id_specialite dans l'URL et que le specialite n'existe pas,
                    flash(f"La spécialité demandée n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_genre" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données spécialité affichées !!", "success")

        except Exception as Exception_specialites_afficher:
            raise ExceptionGenresAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{specialites_afficher.__name__} ; "
                                          f"{Exception_specialites_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("specialite/specialites_afficher.html", data=data_specialites)


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /specialites_ajouter
    
    Test : ex : http://127.0.0.1:5575/specialites_ajouter
    
    Paramètres : sans
    
    But : Ajouter un specialite pour un film
    
    Remarque :  Dans le champ "name_specialite_html" du formulaire "specialite/specialites_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""

# Добавить скрытое поле для id пациента
FormWTFAjouterSpecialites.id_specialite_hidden = HiddenField()

@app.route("/specialites_ajouter", methods=['GET', 'POST'])
def specialites_ajouter_wtf():
    form = FormWTFAjouterSpecialites()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                nom_specialite = form.nom_specialite_wtf.data

                valeurs_insertion = {
                    "value_nom_specialite": nom_specialite
                }
                strsql_insert_specialite = """
                    INSERT INTO t_specialite (nom_specialite)
                    VALUES (%(value_nom_specialite)s)
                """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_specialite, valeurs_insertion)

                flash(f"Spécialité ajoutée : {nom_specialite}!", "success")
                return redirect(url_for('specialites_afficher', order_by='ASC', id_specialite_sel=0))
        except Exception as e:
            raise ExceptionGenresAjouterWtf(f"Erreur lors de l'ajout d'une spécialité : {e}")

    return render_template("specialite/specialites_ajouter_wtf.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /genre_update
    
    Test : ex cliquer sur le menu "specialite" puis cliquer sur le bouton "EDIT" d'un "specialite"
    
    Paramètres : sans
    
    But : Editer(update) un specialite qui a été sélectionné dans le formulaire "specialites_afficher.html"
    
    Remarque :  Dans le champ "nom_genre_update_wtf" du formulaire "specialite/specialite_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/specialite_update_wtf", methods=['GET', 'POST'])
def specialite_update_wtf():
    form = FormWTFUpdateSpecialite()
    if request.method == "POST":
        id_specialite_update = form.id_specialite_hidden.data
    else:
        id_specialite_update = request.values.get('id_specialite_btn_edit_html')

    if request.method == "POST" and form.validate_on_submit():
        try:
            nom_specialite = form.nom_specialite_update_wtf.data

            valeurs_update = {
                "value_id_specialite": id_specialite_update,
                "value_nom_specialite": nom_specialite
            }
            strsql_update_specialite = """
                UPDATE t_specialite
                SET nom_specialite = %(value_nom_specialite)s
                WHERE id_specialite = %(value_id_specialite)s
            """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(strsql_update_specialite, valeurs_update)

            flash(f"Spécialité modifiée : {nom_specialite}!", "success")
            return redirect(url_for('specialites_afficher', order_by='ASC', id_specialite_sel=0))
        except Exception as e:
            raise ExceptionGenresAjouterWtf(f"Erreur lors de la modification de la spécialité : {e}")

    elif request.method == "GET":
        strsql_select_specialite = "SELECT * FROM t_specialite WHERE id_specialite = %(value_id_specialite)s"
        with DBconnection() as mconn_bd:
            mconn_bd.execute(strsql_select_specialite, {"value_id_specialite": id_specialite_update})
            data_specialite = mconn_bd.fetchone()
            if data_specialite:
                form.id_specialite_hidden.data = data_specialite["id_specialite"]
                form.nom_specialite_update_wtf.data = data_specialite["nom_specialite"]

    return render_template("specialite/specialite_update_wtf.html", form_update=form)


"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /specialite_delete
    
    Test : ex. cliquer sur le menu "specialite" puis cliquer sur le bouton "DELETE" d'un "specialite"
    
    Paramètres : sans
    
    But : Effacer(delete) un specialite qui a été sélectionné dans le formulaire "specialites_afficher.html"
    
    Remarque :  Dans le champ "nom_genre_delete_wtf" du formulaire "specialite/genre_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/specialite_delete_wtf", methods=['GET', 'POST'])
def specialite_delete_wtf():
    form_delete = FormWTFDeleteSpecialite()
    id_specialite_delete = request.values.get('id_specialite_btn_delete_html')
    specialite_nom = ""
    if request.method == "POST" and form_delete.validate_on_submit():
        if form_delete.submit_btn_annuler.data:
            return redirect(url_for("specialites_afficher", order_by="ASC", id_specialite_sel=0))
        if form_delete.submit_btn_conf_del.data:
            return render_template("specialite/specialite_delete_wtf.html", form_delete=form_delete, btn_submit_del=True, specialite_nom=specialite_nom)
        if form_delete.submit_btn_del.data:
            try:
                strsql_delete_specialite = "DELETE FROM t_specialite WHERE id_specialite = %(value_id_specialite)s"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_delete_specialite, {"value_id_specialite": id_specialite_delete})
                flash("Spécialité supprimée avec succès!", "success")
                return redirect(url_for('specialites_afficher', order_by="ASC", id_specialite_sel=0))
            except Exception as e:
                raise ExceptionGenresAjouterWtf(f"Erreur lors de la suppression de la spécialité : {e}")

    elif request.method == "GET":
        strsql_select_specialite = "SELECT * FROM t_specialite WHERE id_specialite = %(value_id_specialite)s"
        with DBconnection() as mconn_bd:
            mconn_bd.execute(strsql_select_specialite, {"value_id_specialite": id_specialite_delete})
            data_specialite = mconn_bd.fetchone()
            if data_specialite:
                specialite_nom = data_specialite['nom_specialite']
                form_delete.nom_specialite_delete_wtf.data = specialite_nom

    return render_template("specialite/specialite_delete_wtf.html", form_delete=form_delete, btn_submit_del=False, specialite_nom=specialite_nom, data_films_associes=None)

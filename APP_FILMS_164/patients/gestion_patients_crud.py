"""Gestion des "routes" FLASK et des données pour les medecin.
Fichier : gestion_patients_crud.py
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
from APP_FILMS_164.patients.gestion_patients_wtf_forms import FormWTFAjouterPatients
from APP_FILMS_164.patients.gestion_patients_wtf_forms import FormWTFDeletePatient
from APP_FILMS_164.patients.gestion_patients_wtf_forms import FormWTFUpdatePatient
from wtforms import HiddenField

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /patients_afficher
    
    Test : ex : http://127.0.0.1:5575/patients_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_patient_sel = 0 >> tous les patients.
                id_patient_sel = "n" affiche le patient dont l'id est "n"
"""


@app.route("/patients_afficher/<string:order_by>/<int:id_patient_sel>", methods=['GET', 'POST'])
def patients_afficher(order_by, id_patient_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_patient_sel == 0:
                    strsql_patients_afficher = """SELECT * FROM t_pationt"""
                    mc_afficher.execute(strsql_patients_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_genre"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du patient sélectionné avec un nom de variable
                    valeur_id_patient_selected_dictionnaire = {"value_id_patient_selected": id_patient_sel}
                    strsql_patients_afficher = """SELECT * FROM t_pationt"""

                    mc_afficher.execute(strsql_patients_afficher, valeur_id_patient_selected_dictionnaire)
                else:
                    strsql_patients_afficher = """SELECT * FROM t_pationt"""

                    mc_afficher.execute(strsql_patients_afficher)

                data_patients = mc_afficher.fetchall()

                print("data_genres ", data_patients, " Type : ", type(data_patients))

                # Différencier les messages si la table est vide.
                if not data_patients and id_patient_sel == 0:
                    flash("""La table "t_pationt" est vide. !!""", "warning")
                elif not data_patients and id_patient_sel > 0:
                    # Si l'utilisateur change l'id_patient dans l'URL et que le patient n'existe pas,
                    flash(f"Le patient demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_genre" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données medecin affichés !!", "success")

        except Exception as Exception_patients_afficher:
            raise ExceptionGenresAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{patients_afficher.__name__} ; "
                                          f"{Exception_patients_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("patient/patients_afficher.html", data=data_patients)


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /patients_ajouter
    
    Test : ex : http://127.0.0.1:5575/patients_ajouter
    
    Paramètres : sans
    
    But : Ajouter un patient pour un film
    
    Remarque :  Dans le champ "name_patient_html" du formulaire "patient/patients_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""

# Добавить скрытое поле для id пациента
FormWTFAjouterPatients.id_patient_hidden = HiddenField()

@app.route("/patients_ajouter", methods=['GET', 'POST'])
def patients_ajouter_wtf():
    form = FormWTFAjouterPatients()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                nom_patient = form.nom_patient_wtf.data
                # Получите остальные поля из формы, если они есть
                prenome_patient = request.form.get("prenome_patient_wtf")
                date_naissance = request.form.get("date_naissance_wtf")
                adresse = request.form.get("adresse_wtf")
                telephone = request.form.get("telephone_wtf")
                email = request.form.get("email_wtf")

                valeurs_insertion = {
                    "value_nom_pationt": nom_patient,
                    "value_prenome_pationt": prenome_patient,
                    "value_date_naissance": date_naissance,
                    "value_adresse": adresse,
                    "value_telephone": telephone,
                    "value_email": email
                }
                strsql_insert_patient = """
                    INSERT INTO t_pationt (nom_pationt, prenome_pationt, date_naissance, adresse, telephone, email)
                    VALUES (%(value_nom_pationt)s, %(value_prenome_pationt)s, %(value_date_naissance)s, %(value_adresse)s, %(value_telephone)s, %(value_email)s)
                """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_patient, valeurs_insertion)

                flash(f"Пациент успешно добавлен: {nom_patient}!", "success")
                return redirect(url_for('patients_afficher', order_by='ASC', id_patient_sel=0))
        except Exception as e:
            raise ExceptionGenresAjouterWtf(f"Erreur при добавлении нового пациента : {e}")

    return render_template("patient/patients_ajouter_wtf.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /genre_update
    
    Test : ex cliquer sur le menu "medecin" puis cliquer sur le bouton "EDIT" d'un "patient"
    
    Paramètres : sans
    
    But : Editer(update) un patient qui a été sélectionné dans le formulaire "patients_afficher.html"
    
    Remarque :  Dans le champ "nom_genre_update_wtf" du formulaire "medecin/patient_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/patient_update_wtf", methods=['GET', 'POST'])
def patient_update_wtf():
    from APP_FILMS_164.patients.gestion_patients_wtf_forms import FormWTFUpdatePatient
    form = FormWTFUpdatePatient()
    if request.method == "POST":
        id_patient_update = form.id_patient_hidden.data
    else:
        id_patient_update = request.values.get('id_patient_btn_edit_html')

    if request.method == "POST" and form.validate_on_submit():
        try:
            nom_patient = form.nom_patient_update_wtf.data
            prenome_patient = form.prenome_patient_update_wtf.data
            date_naissance = form.date_naissance_update_wtf.data
            adresse = form.adresse_update_wtf.data
            telephone = form.telephone_update_wtf.data
            email = form.email_update_wtf.data

            valeurs_update = {
                "value_id_pationt": id_patient_update,
                "value_nom_pationt": nom_patient,
                "value_prenome_pationt": prenome_patient,
                "value_date_naissance": date_naissance,
                "value_adresse": adresse,
                "value_telephone": telephone,
                "value_email": email
            }
            strsql_update_patient = """
                UPDATE t_pationt
                SET nom_pationt = %(value_nom_pationt)s,
                    prenome_pationt = %(value_prenome_pationt)s,
                    date_naissance = %(value_date_naissance)s,
                    adresse = %(value_adresse)s,
                    telephone = %(value_telephone)s,
                    email = %(value_email)s
                WHERE id_pationt = %(value_id_pationt)s
            """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(strsql_update_patient, valeurs_update)

            flash(f"Данные пациента успешно обновлены: {nom_patient}!", "success")
            return redirect(url_for('patients_afficher', order_by='ASC', id_patient_sel=0))
        except Exception as e:
            raise ExceptionGenresAjouterWtf(f"Ошибка при обновлении пациента : {e}")

    elif request.method == "GET":
        strsql_select_patient = "SELECT * FROM t_pationt WHERE id_pationt = %(value_id_pationt)s"
        with DBconnection() as mconn_bd:
            mconn_bd.execute(strsql_select_patient, {"value_id_pationt": id_patient_update})
            data_patient = mconn_bd.fetchone()
            if data_patient:
                form.id_patient_hidden.data = data_patient["id_pationt"]
                form.nom_patient_update_wtf.data = data_patient["nom_pationt"]
                form.prenome_patient_update_wtf.data = data_patient["prenome_pationt"]
                form.date_naissance_update_wtf.data = data_patient["date_naissance"]
                form.adresse_update_wtf.data = data_patient["adresse"]
                form.telephone_update_wtf.data = data_patient["telephone"]
                form.email_update_wtf.data = data_patient["email"]

    return render_template("patient/patient_update_wtf.html", form_update=form)


"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /patient_delete
    
    Test : ex. cliquer sur le menu "medecin" puis cliquer sur le bouton "DELETE" d'un "patient"
    
    Paramètres : sans
    
    But : Effacer(delete) un patient qui a été sélectionné dans le formulaire "patients_afficher.html"
    
    Remarque :  Dans le champ "nom_genre_delete_wtf" du formulaire "medecin/genre_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/patient_delete_wtf", methods=['GET', 'POST'])
def patient_delete_wtf():
    from APP_FILMS_164.patients.gestion_patients_wtf_forms import FormWTFDeletePatient
    id_patient_delete = request.values.get('id_patient_btn_delete_html')
    form_delete = FormWTFDeletePatient()
    patient_nom = ""
    if request.method == "POST" and form_delete.validate_on_submit():
        if form_delete.submit_btn_annuler.data:
            return redirect(url_for("patients_afficher", order_by="ASC", id_patient_sel=0))
        if form_delete.submit_btn_conf_del.data:
            return render_template("patient/patient_delete_wtf.html", form_delete=form_delete, btn_submit_del=True, patient_nom=patient_nom)
        if form_delete.submit_btn_del.data:
            try:
                strsql_delete_patient = "DELETE FROM t_pationt WHERE id_pationt = %(value_id_pationt)s"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_delete_patient, {"value_id_pationt": id_patient_delete})
                flash("Пациент успешно удалён!", "success")
                return redirect(url_for('patients_afficher', order_by="ASC", id_patient_sel=0))
            except Exception as e:
                raise ExceptionGenresAjouterWtf(f"Ошибка при удалении пациента : {e}")

    elif request.method == "GET":
        strsql_select_patient = "SELECT * FROM t_pationt WHERE id_pationt = %(value_id_pationt)s"
        with DBconnection() as mconn_bd:
            mconn_bd.execute(strsql_select_patient, {"value_id_pationt": id_patient_delete})
            data_patient = mconn_bd.fetchone()
            if data_patient:
                patient_nom = f"{data_patient['nom_pationt']} {data_patient['prenome_pationt']}"
                form_delete.nom_patient_delete_wtf.data = patient_nom

    return render_template("patient/patient_delete_wtf.html", form_delete=form_delete, btn_submit_del=False, patient_nom=patient_nom, data_films_associes=None)

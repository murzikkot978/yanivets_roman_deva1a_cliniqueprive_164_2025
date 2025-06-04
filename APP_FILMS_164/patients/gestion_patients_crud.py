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


@app.route("/patients_ajouter", methods=['GET', 'POST'])
def patients_ajouter_wtf():
    form = FormWTFAjouterPatients()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                name_patient_wtf = form.nom_patient_wtf.data
                name_patient = name_patient_wtf.lower()
                valeurs_insertion_dictionnaire = {"value_intitule_genre": name_patient}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)
                strsql_insert_patient = """INSERT INTO t_medecin (`id_medecin`, `nom_medecin`, `prenome_medecin`, `telephone`, `fk_specialite`, `email`) VALUES (NULL,%(value_intitule_genre)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_patient, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('patients_afficher', order_by='DESC', id_patient_sel=0))

        except Exception as Exception_patients_ajouter_wtf:
            raise ExceptionGenresAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{patients_ajouter_wtf.__name__} ; "
                                            f"{Exception_patients_ajouter_wtf}")

    return render_template("medecin/patients_ajouter_wtf.html", form=form)


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


@app.route("/patient_update", methods=['GET', 'POST'])
def patient_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_genre"
    id_patient_update = request.values['id_patient_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdatePatient()
    try:
        # 2023.05.14 OM S'il y a des listes déroulantes dans le formulaire
        # La validation pose quelques problèmes
        if request.method == "POST" and form_update.submit.data:
            # Récupèrer la valeur du champ depuis "patient_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            name_patient_update = form_update.nom_patient_update_wtf.data
            name_patient_update = name_patient_update.lower()
            date_patient_essai = form_update.date_patient_wtf_essai.data

            valeur_update_dictionnaire = {"value_id_genre": id_patient_update,
                                          "value_name_genre": name_patient_update,
                                          "value_date_genre_essai": date_patient_essai
                                          }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_intitulegenre = """UPDATE t_pationt SET intitule_genre = %(value_name_patient)s, 
            date_ins_genre = %(value_date_genre_essai)s WHERE id_genre = %(value_id_genre)s """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_intitulegenre, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_genre_update"
            return redirect(url_for('patients_afficher', order_by="ASC", id_patient_sel=id_patient_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_genre" et "intitule_genre" de la "t_genre"
            str_sql_id_patient = "SELECT id_genre, intitule_genre, date_ins_genre FROM t_genre " \
                               "WHERE id_genre = %(value_id_genre)s"
            valeur_select_dictionnaire = {"value_id_patient": id_patient_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_patient, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom patient" pour l'UPDATE
            data_nom_genre = mybd_conn.fetchone()
            print("data_nom_genre ", data_nom_genre, " type ", type(data_nom_genre), " patient ",
                  data_nom_genre["intitule_genre"])

            # Afficher la valeur sélectionnée dans les champs du formulaire "patient_update_wtf.html"
            form_update.nom_genre_update_wtf.data = data_nom_genre["intitule_genre"]
            form_update.date_genre_wtf_essai.data = data_nom_genre["date_ins_genre"]

    except Exception as Exception_patient_update_wtf:
        raise ExceptionGenreUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{patient_update_wtf.__name__} ; "
                                      f"{Exception_patient_update_wtf}")

    return render_template("medecin/patient_update_wtf.html", form_update=form_update)


"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /patient_delete
    
    Test : ex. cliquer sur le menu "medecin" puis cliquer sur le bouton "DELETE" d'un "patient"
    
    Paramètres : sans
    
    But : Effacer(delete) un patient qui a été sélectionné dans le formulaire "patients_afficher.html"
    
    Remarque :  Dans le champ "nom_genre_delete_wtf" du formulaire "medecin/genre_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/patient_delete", methods=['GET', 'POST'])
def patient_delete_wtf():
    data_films_attribue_patient_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_genre"
    id_patient_delete = request.values['id_patient_btn_delete_html']

    # Objet formulaire pour effacer le patient sélectionné.
    form_delete = FormWTFDeletePatient()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("patients_afficher", order_by="ASC", id_patient_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "medecin/genre_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_films_attribue_genre_delete = session['data_films_attribue_genre_delete']
                print("data_films_attribue_genre_delete ", data_films_attribue_genre_delete)

                flash(f"Effacer le patient de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer patient" qui va irrémédiablement EFFACER le patient
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_genre": id_patient_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_films_genre = """DELETE FROM t_genre_film WHERE fk_genre = %(value_id_genre)s"""
                str_sql_delete_idgenre = """DELETE FROM t_genre WHERE id_genre = %(value_id_genre)s"""
                # Manière brutale d'effacer d'abord la "fk_genre", même si elle n'existe pas dans la "t_genre_film"
                # Ensuite on peut effacer le patient vu qu'il n'est plus "lié" (INNODB) dans la "t_genre_film"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_films_genre, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_idgenre, valeur_delete_dictionnaire)

                flash(f"Genre définitivement effacé !!", "success")
                print(f"Genre définitivement effacé !!")

                # afficher les données
                return redirect(url_for('patients_afficher', order_by="ASC", id_patient_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_genre": id_patient_delete}
            print(id_patient_delete, type(id_patient_delete))

            # Requête qui affiche tous les facture qui ont le patient que l'utilisateur veut effacer
            str_sql_genres_films_delete = """SELECT id_genre_film, nom_film, id_genre, intitule_genre FROM t_genre_film 
                                            INNER JOIN t_film ON t_genre_film.fk_film = t_film.id_film
                                            INNER JOIN t_genre ON t_genre_film.fk_genre = t_genre.id_genre
                                            WHERE fk_genre = %(value_id_genre)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_genres_films_delete, valeur_select_dictionnaire)
                data_films_attribue_genre_delete = mydb_conn.fetchall()
                print("data_films_attribue_genre_delete...", data_films_attribue_genre_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "medecin/genre_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_films_attribue_genre_delete'] = data_films_attribue_genre_delete

                # Opération sur la BD pour récupérer "id_genre" et "intitule_genre" de la "t_genre"
                str_sql_id_patient = "SELECT id_genre, intitule_genre FROM t_genre WHERE id_genre = %(value_id_genre)s"

                mydb_conn.execute(str_sql_id_patient, valeur_select_dictionnaire)
                # Une seule valeur est suffisante "fetchone()",
                # vu qu'il n'y a qu'un seul champ "nom patient" pour l'action DELETE
                data_nom_genre = mydb_conn.fetchone()
                print("data_nom_genre ", data_nom_genre, " type ", type(data_nom_genre), " patient ",
                      data_nom_genre["intitule_genre"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "genre_delete_wtf.html"
            form_delete.nom_genre_delete_wtf.data = data_nom_genre["intitule_genre"]

            # Le bouton pour l'action "DELETE" dans le form. "genre_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_genre_delete_wtf:
        raise ExceptionGenreDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{patient_delete_wtf.__name__} ; "
                                      f"{Exception_genre_delete_wtf}")

    return render_template("medecin/genre_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_films_associes=data_films_attribue_genre_delete)

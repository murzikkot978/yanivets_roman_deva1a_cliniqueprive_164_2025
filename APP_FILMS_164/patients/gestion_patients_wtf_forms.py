"""
    Fichier : gestion_genres_wtf_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms import SubmitField, HiddenField
from wtforms.validators import Length, InputRequired, DataRequired
from wtforms.validators import Regexp


class FormWTFAjouterPatients(FlaskForm):
    """
        Dans le formulaire "genres_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_patient_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_patient_wtf = StringField("Prénom", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                    Regexp(nom_patient_regexp, message="Nom incorrect")])
    prenome_patient_wtf = StringField("Nom", validators=[Length(min=2, max=20, message="min 2 max 20")])
    date_naissance_wtf = DateField("Дата рождения", validators=[InputRequired("Дата обязательна")])
    adresse_wtf = StringField("Adresse", validators=[Length(min=2, max=50, message="min 2 max 50")])
    telephone_wtf = StringField("Téléphone", validators=[Length(min=6, max=20, message="min 6 max 20")])
    email_wtf = StringField("Email", validators=[Length(min=5, max=100, message="min 5 max 100")])
    id_patient_hidden = HiddenField()
    submit = SubmitField("Enregistrer le patient")


class FormWTFUpdatePatient(FlaskForm):
    """
        Formulaire complet pour l'édition d'un patient (как для врача).
    """
    nom_patient_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_patient_update_wtf = StringField("Prénom", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                           Regexp(nom_patient_update_regexp, message="Nom incorrect")])
    prenome_patient_update_wtf = StringField("Nom", validators=[Length(min=2, max=20, message="min 2 max 20")])
    date_naissance_update_wtf = DateField("Дата рождения", validators=[InputRequired("Дата обязательна")])
    adresse_update_wtf = StringField("Adresse", validators=[Length(min=2, max=50, message="min 2 max 50")])
    telephone_update_wtf = StringField("Téléphone", validators=[Length(min=6, max=20, message="min 6 max 20")])
    email_update_wtf = StringField("Email", validators=[Length(min=5, max=100, message="min 5 max 100")])
    id_patient_hidden = HiddenField()
    submit = SubmitField("Enregistrer les modifications")


class FormWTFDeletePatient(FlaskForm):
    """
        Dans le formulaire "genre_delete_wtf.html"

        nom_genre_delete_wtf : Champ qui reçoit la valeur du genre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "genre".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_genre".
    """
    nom_patient_delete_wtf = StringField("Supprimer ce patient")
    submit_btn_del = SubmitField("Supprimer le patient")
    submit_btn_conf_del = SubmitField("Êtes-vous sûr de vouloir supprimer ?")
    submit_btn_annuler = SubmitField("Annuler")

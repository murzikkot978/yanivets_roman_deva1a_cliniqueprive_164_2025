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


class FormWTFAjouterSpecialites(FlaskForm):
    """
        Formulaire pour ajouter une spécialité.
    """
    nom_specialite_wtf = StringField("Nom de la spécialité", validators=[Length(min=2, max=50, message="min 2 max 50")])
    id_specialite_hidden = HiddenField()
    submit = SubmitField("Enregistrer la spécialité")


class FormWTFUpdateSpecialite(FlaskForm):
    """
        Formulaire pour modifier une spécialité.
    """
    nom_specialite_update_wtf = StringField("Nom de la spécialité", validators=[Length(min=2, max=50, message="min 2 max 50")])
    id_specialite_hidden = HiddenField()
    submit = SubmitField("Enregistrer les modifications")


class FormWTFDeleteSpecialite(FlaskForm):
    """
        Formulaire pour supprimer une spécialité.
    """
    nom_specialite_delete_wtf = StringField("Supprimer cette spécialité")
    submit_btn_del = SubmitField("Supprimer la spécialité")
    submit_btn_conf_del = SubmitField("Êtes-vous sûr de vouloir supprimer ?")
    submit_btn_annuler = SubmitField("Annuler")

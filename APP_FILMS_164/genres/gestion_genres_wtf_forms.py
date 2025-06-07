"""
    Fichier : gestion_genres_wtf_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, HiddenField
from wtforms import SubmitField
from wtforms.validators import Length, InputRequired, DataRequired
from wtforms.validators import Regexp


class FormWTFAjouterGenres(FlaskForm):
    """
        Dans le formulaire "genres_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_medecin_wtf = StringField("Prénom du médecin",
                                  validators=[Length(min=2, max=50, message="De 2 à 50 caractères")])
    prenome_medecin_wtf = StringField("Nom du médecin",
                                      validators=[Length(min=2, max=50, message="De 2 à 50 caractères")])
    telephone_wtf = StringField("Téléphone",
                                validators=[Regexp(r'^\d{10}$', message="Entrez un numéro de téléphone à 10 chiffres")])
    email_wtf = StringField("Email", validators=[Length(min=5, max=100, message="Jusqu'à 100 caractères")])
    specialite_wtf = SelectField("Spécialité du médecin", coerce=int, validators=[DataRequired(message="La spécialité est obligatoire !")])
    submit = SubmitField("Enregistrer le médecin")


class FormWTFDeleteGenre(FlaskForm):
    """
        Dans le formulaire "genre_delete_wtf.html"

        nom_genre_delete_wtf : Champ qui reçoit la valeur du genre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "genre".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_genre".
    """
    nom_genre_delete_wtf = StringField("Supprimer ce médecin")
    submit_btn_del = SubmitField("Supprimer le médecin")
    submit_btn_conf_del = SubmitField("Êtes-vous sûr de vouloir supprimer ?")
    submit_btn_annuler = SubmitField("Annuler")


class FormWTFUpdateMedecin(FlaskForm):
    nom_medecin_update_wtf = StringField("Prénom", validators=[Length(min=2, max=50, message="De 2 à 50 caractères")])
    prenome_medecin_update_wtf = StringField("Nom", validators=[Length(min=2, max=50, message="De 2 à 50 caractères")])
    telephone_update_wtf = StringField("Téléphone", validators=[Regexp(r'^\d{10}$', message="Entrez un numéro de téléphone à 10 chiffres")])
    email_update_wtf = StringField("Email", validators=[Length(min=5, max=100, message="Jusqu'à 100 caractères")])
    specialite_update_wtf = SelectField("Spécialité", coerce=int, validators=[DataRequired(message="La spécialité est obligatoire !")])
    id_medecin_hidden = HiddenField()
    submit = SubmitField("Enregistrer les modifications")

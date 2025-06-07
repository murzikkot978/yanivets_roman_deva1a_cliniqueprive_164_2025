"""
    Fichier : gestion_consultations_wtf_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, HiddenField
from wtforms import SubmitField
from wtforms.validators import Length, InputRequired, DataRequired
from wtforms.validators import Regexp


class FormWTFAjouterConsultations(FlaskForm):
    """
        Formulaire pour ajouter une consultation.
    """
    fk_medecin = SelectField("Médecin", coerce=int, validators=[DataRequired()])
    fk_patient = SelectField("Patient", coerce=int, validators=[DataRequired()])
    date_consultation = DateField("Date de consultation", validators=[InputRequired("Date obligatoire")])
    id_consultation_hidden = HiddenField()
    submit = SubmitField("Ajouter la consultation")


class FormWTFUpdateConsultation(FlaskForm):
    """
        Formulaire pour modifier une consultation.
    """
    fk_medecin = SelectField("Médecin", coerce=int, validators=[DataRequired()])
    fk_patient = SelectField("Patient", coerce=int, validators=[DataRequired()])
    date_consultation = DateField("Date de consultation", validators=[InputRequired("Date obligatoire")])
    id_consultation_hidden = HiddenField()
    submit = SubmitField("Enregistrer les modifications")


class FormWTFDeleteConsultation(FlaskForm):
    """
        Formulaire pour supprimer une consultation.
    """
    nom_genre_delete_wtf = StringField("Information sur la consultation")
    submit_btn_del = SubmitField("Supprimer la consultation")
    submit_btn_conf_del = SubmitField("Êtes-vous sûr de vouloir supprimer ?")
    submit_btn_annuler = SubmitField("Annuler")

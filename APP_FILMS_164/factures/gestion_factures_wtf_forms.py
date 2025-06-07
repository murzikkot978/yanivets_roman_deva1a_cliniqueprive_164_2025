"""
    Fichier : gestion_genres_wtf_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, HiddenField, IntegerField
from wtforms import SubmitField
from wtforms.validators import Length, InputRequired, DataRequired
from wtforms.validators import Regexp, NumberRange


class FormWTFAjouterFactures(FlaskForm):
    """
        Dans le formulaire "genres_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    fk_pationt = SelectField("Пациент", coerce=int, validators=[DataRequired()])
    montant = IntegerField("Сумма", validators=[InputRequired(), NumberRange(min=0)])
    date_emission = DateField("Дата выставления", validators=[InputRequired("Дата обязательна")])
    fk_consultation = SelectField("Консультация", coerce=int, validators=[DataRequired()])
    id_facture_hidden = HiddenField()
    submit = SubmitField("Добавить фактуру")


class FormWTFDeleteFacture(FlaskForm):
    """
        Dans le formulaire "genre_delete_wtf.html"

        nom_genre_delete_wtf : Champ qui reçoit la valeur du genre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "genre".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_genre".
    """
    nom_genre_delete_wtf = StringField("Информация о фактуре")
    submit_btn_del = SubmitField("Удалить фактуру")
    submit_btn_conf_del = SubmitField("Вы уверены, что хотите удалить?")
    submit_btn_annuler = SubmitField("Отмена")


class FormWTFUpdateFacture(FlaskForm):
    fk_pationt = SelectField("Пациент", coerce=int, validators=[DataRequired()])
    montant = IntegerField("Сумма", validators=[InputRequired(), NumberRange(min=0)])
    date_emission = DateField("Дата выставления", validators=[InputRequired("Дата обязательна")])
    fk_consultation = SelectField("Консультация", coerce=int, validators=[DataRequired()])
    id_facture_hidden = HiddenField()
    submit = SubmitField("Сохранить изменения")

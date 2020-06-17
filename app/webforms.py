from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectMultipleField, widgets


class ShufflerForm(FlaskForm):
    playlists = SelectMultipleField('Select Playlists', widget=widgets.ListWidget(prefix_label=False),
                                    option_widget=widgets.CheckboxInput(), choices=[])
    submit = SubmitField('SHUFFLE')

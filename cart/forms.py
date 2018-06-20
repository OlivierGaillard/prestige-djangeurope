from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import TabHolder, Tab, FormActions
from crispy_forms.layout import Submit, Layout, Fieldset, Field
from django import forms
from django.utils.translation import ugettext_lazy as _

from django.shortcuts import reverse
from inventory.models import Article
from .models import Vente, Client, Paiement

class VenteCreateForm(forms.ModelForm):
    class Meta:
        model = Vente
        fields = ('branch', 'date', 'client', 'montant')
        widgets = {
            'date': forms.DateTimeInput(
                attrs={'id': 'datetimepicker_vente'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(VenteCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "POST"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-4'
        self.helper.layout.append(
            FormActions(
                Submit('save', 'Submit'),
            )
        )

class VenteUpdateForm(forms.ModelForm):
    class Meta:
        model = Vente
        fields = ('date', 'client', 'montant', 'reglement_termine')
        widgets = {
            'date': forms.DateTimeInput(
                attrs={'id': 'datetimepicker_vente'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(VenteUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "POST"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-4'
        self.helper.layout.append(
            FormActions(
                Submit('save', 'Submit'),
            )
        )


class VenteDeleteForm(forms.ModelForm):
    class Meta:
        model = Vente
        fields = ('date', 'client', 'montant', 'reglement_termine')

    def __init__(self, *args, **kwargs):
        super(VenteDeleteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "POST"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-4'
        self.helper.layout.append(
            FormActions(
                Submit('save', 'Submit'),
            )
        )


class ClientCreateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('title', 'nom', 'prenom', 'tel')

    def __init__(self, *args, **kwargs):
        super(ClientCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "POST"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-4'
        self.helper.layout.append(
            FormActions(
                Submit('save', 'Submit'),
            )
        )

class ClientUpdateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('title', 'nom', 'prenom', 'tel')
    def __init__(self, *args, **kwargs):
        super(ClientUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "POST"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-4'
        self.helper.layout.append(
            FormActions(
                Submit('save', 'Submit'),
            )
        )




class PaiementCreateForm(forms.Form):
    date = forms.DateTimeField(required=True, widget=forms.DateTimeInput(
        attrs={'id': 'datetimepicker_vente'}
        ))
    payment_amount = forms.DecimalField(required=True, label=_("Amount"))


    def __init__(self, *args, **kwargs):
        super(PaiementCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "POST"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-4'
        self.helper.layout.append(
            FormActions(
                Submit('save', 'Submit'),
            )
        )

    #
    #
    # def clean(self):
    #     cleaned_data = super(PaiementCreateForm, self).clean()
    #     vente_pk = cleaned_data['vente']
    #     payment_amount = cleaned_data['payment_amount']
    #     vente = Vente.objects.get(pk=vente_pk.pk)
    #     if float(payment_amount) > vente.solde_paiements():
    #         #self.add_error('montant', 'Montant dépasse le solde!')
    #         raise forms.ValidationError('Le montant dépasse le solde qui reste à payer!', code='toogreat')
    #     return cleaned_data









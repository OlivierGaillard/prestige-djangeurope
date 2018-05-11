from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import TabHolder, Tab, FormActions
from crispy_forms.layout import Submit, Layout, Fieldset, Field
from django import forms
from django.shortcuts import reverse
from .models import Article, Branch, Category, Arrivage, Losses
from django.utils.translation import ugettext_lazy as _


class ArrivalUpdateForm(forms.ModelForm):
    class Meta:
        model = Arrivage
        fields = ('nom', 'date_arrivee')
        widgets = {
            'date_arrivee': forms.DateInput(format='%d-%m-%Y',
                attrs={'id': 'datetimepicker_arrival'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(ArrivalUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "POST"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-4'
        self.helper.layout.append(
            FormActions(
                Submit('save', 'Submit'),
            )
        )


class ArrivalCreateForm(forms.ModelForm):
    class Meta:
        model = Arrivage
        fields = ('nom', 'date_arrivee')
        widgets = {
            'date_arrivee': forms.DateInput(format='%d-%m-%Y',
                                            attrs={'id': 'datetimepicker_arrival'}
                                            ),
        }

    def __init__(self, *args, **kwargs):
        super(ArrivalCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "POST"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-4'
        self.helper.layout.append(
            FormActions(
                Submit('save', 'Submit'),
            )
        )

class ArticleDeleteForm(forms.Form):
    delete_purchasing_costs = forms.BooleanField(required=False, label=_("Delete Purchasing Costs too?"))

    def __init__(self, *args, **kwargs):
        super(ArticleDeleteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "POST"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-4'
        self.helper.layout.append(
            FormActions(
                Submit('save', 'Submit'),
            )
        )



class CategoryFormCreate(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super(CategoryFormCreate, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "POST"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-4'
        self.helper.layout.append(
            FormActions(
                Submit('save', 'Submit'),
            )
        )

class CategoryFormUpdate(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super(CategoryFormUpdate, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "POST"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-4'
        self.helper.layout.append(
            FormActions(
                Submit('save', 'Submit'),
            )
        )


class CategoryFormDelete(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super(CategoryFormDelete, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "POST"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-4'
        self.helper.layout.append(
            FormActions(
                Submit('save', 'Submit'),
            )
        )


class BranchCreateForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super(BranchCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "POST"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-4'
        self.helper.layout.append(
            FormActions(
                Submit('save', 'Submit'),
            )
        )

class BranchUpdateForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super(BranchUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "POST"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-4'
        self.helper.layout.append(
            FormActions(
                Submit('save', 'Submit'),
            )
        )



class ArticleUpdateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('branch', 'category', 'nom', 'solde', 'purchasing_price', 'selling_price')

    def __init__(self, *args, **kwargs):
        super(ArticleUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "POST"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-4'
        self.helper.layout.append(
            FormActions(
                Submit('save', 'Submit'),
            )
        )


class ArticleCreateForm(forms.ModelForm):
    #quantite = forms.IntegerField(min_value=1, required=True, label="Quantité", initial=0,
    #                              help_text="Quantité en stock (peut différer de la quantité achetée)")
    new_marque = forms.CharField(max_length=100, required=False, help_text='Pour entrer une nouvelle marque')

    class Meta:
        model = Article
        fields = ('category', 'type_client', 'genre_article', 'nom', 'marque', 'quantite', 'prix_unitaire', 'prix_total',
                  'arrivage', 'entreprise')

        widgets = {
            'type_client': forms.RadioSelect,
        }


    def __init__(self, *args, **kwargs):
        super(ArticleCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "POST"
        self.helper.form_action = reverse('inventory:article_create')
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-4'
        self.helper.layout = Layout(
            TabHolder(
                Tab('Fiche article',
                    'category', 'nom', 'arrivage', 'entreprise',
                    'quantite', 'prix_unitaire', 'prix_total',),

                Tab('Classification',
                    'type_client', 'marque', 'new_marque',
                    ),
            ),
            #Submit('submit', u'Submit', css_class='btn btn-success'),
        )
        self.helper.layout.append(
            FormActions(
                Submit('save', 'Submit'),
            )
        )

#        self.helper.add_input(Submit('Submit', 'submit'))

        # if self.user:
        #     user_enterprise = Employee.get_enterprise_of_current_user(self.user)
        #     self.fields['arrivage'].queryset = Arrivage.objects.filter(enterprise=user_enterprise)
        #     self.fields['product_owner'].queryset = Enterprise.objects.filter(pk=user_enterprise.pk)

    # def clean(self):
    #     cleaned_data = super(ArticleCreateForm, self).clean()
    #     print("in clean")
    #     # marque_ref = cleaned_data.get('marque_ref', '')
    #     # if marque_ref is None:
    #     #     marque = cleaned_data.get('marque', '')
    #     #     if len(marque) == 0:
    #     #         msg = "Vous devez choisir une marque ou en créer une en renseignant le champ 'marque'. "
    #     #         raise forms.ValidationError(msg)
    #     return cleaned_data
    #
class AddPhotoForm(forms.Form):
    image   = forms.ImageField()


class ArticleLossesForm(forms.Form):
    losses = forms.IntegerField(required=True, min_value=1, help_text=_("Total of articles lost"))
    amount_losses = forms.DecimalField(required=True, min_value=0.01, help_text=_("Total of money lost"))


    def __init__(self, *args, **kwargs):
        super(ArticleLossesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "POST"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-4'
        self.helper.layout.append(
            FormActions(
                Submit('save', 'Submit'),
            )
        )

class ArticleLossesUpdateForm(forms.ModelForm):
    class Meta:
        model = Losses
        fields = ('amount_losses', 'date', 'loss_type', 'note')
        widgets = {
            'date': forms.DateInput(
                attrs={'id': 'datetimepicker_es'}
            ),
        }


    def __init__(self, *args, **kwargs):
        super(ArticleLossesUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "POST"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-4'
        self.helper.layout.append(
            FormActions(
                Submit('save', 'Submit'),
            )
        )


from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import TabHolder, Tab, FormActions
from crispy_forms.layout import Submit, Layout, Fieldset, Field, HTML
from django import forms
from django.shortcuts import reverse
from django.conf import settings
from .models import Article, Branch, Category, Arrivage, Losses
from django.utils.translation import ugettext_lazy as _
import os
import logging
logger = logging.getLogger('django')


class UploadPicturesZipForm(forms.Form):
    pictures_zip = forms.FileField()

    def __init__(self, *args, **kwargs):
        super(UploadPicturesZipForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "POST"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-4'

        pictures_dir = os.path.join(settings.MEDIA_ROOT, 'tmp')
        li = os.listdir(pictures_dir)
        if len(li) > 0:
            msg = _('They are already uploaded pictures. Please generate the articles before uploading new ones.')
            self.helper.layout = Layout(
                HTML("<div class='alert alert-warning'>%s</div>" % msg)
            )
        else:
            self.helper.layout.append(
                FormActions(
                    Submit('save', _('Upload')),
                )
            )


    def clean(self):
        cleaned_data = super(UploadPicturesZipForm, self).clean()
        zip_file = cleaned_data['pictures_zip']
        if not zip_file.name.split('.')[1] == 'zip':
            self.add_error('pictures_zip', _("File ends not with extension '.zip'."))
        return cleaned_data



class HandlePicturesForm(forms.Form):

    branch   = forms.ModelChoiceField(label=_('Branch'), required=False, queryset=Branch.objects.all())
    arrival  = forms.ModelChoiceField(label=_('Arrival'), queryset=Arrivage.objects.all())
    category = forms.ModelChoiceField(label=_('Category'), required=False, queryset=Category.objects.all())

    def __init__(self, *args, **kwargs):
        super(HandlePicturesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "POST"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-4'
        self.helper.layout.append(
            FormActions(
                Submit('save', _('Generate')),
            )
        )


class ArrivalUpdateForm(forms.ModelForm):
    class Meta:
        model = Arrivage
        fields = ('nom', 'date_arrivee', 'proprietaire')
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

# class ArticleDeleteForm(forms.Form):
#     delete_purchasing_costs = forms.BooleanField(required=False, label=_("Delete Purchasing Costs too?"))
#
#     def __init__(self, *args, **kwargs):
#         super(ArticleDeleteForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper(self)
#         self.helper.form_method = "POST"
#         self.helper.form_class = 'form-horizontal'
#         self.helper.label_class = 'col-sm-2'
#         self.helper.field_class = 'col-sm-4'
#         self.helper.layout.append(
#             FormActions(
#                 Submit('save', 'Submit'),
#             )
#         )



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
        fields = ('branch', 'category', 'type_client', 'genre_article', 'name', 'marque', 'quantity', 'purchasing_price',
                  'selling_price', 'arrivage', 'entreprise')
        #fields = ('branch', 'category', 'nom', 'solde', 'purchasing_price', 'selling_price')

        widgets = {
            'type_client': forms.RadioSelect,
        }

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
        fields = ('branch', 'category', 'type_client', 'genre_article', 'name', 'marque', 'quantity', 'purchasing_price',
                  'selling_price', 'arrivage', 'entreprise')

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
                    'quantity', 'purchasing_price', 'selling_price',),

                Tab('Classification',
                    'branch', 'type_client', 'marque', 'new_marque',
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


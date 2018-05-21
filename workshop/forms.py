from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import TabHolder, Tab, FormActions
from crispy_forms.layout import Submit, Layout, Fieldset, Field
from django import forms
from .models import Product, ProductCategory


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('deadline', 'order_date', 'client', 'work_state', 'name', 'product_category', 'selling_price', 'note', 'photo')
        widgets = {
            'deadline': forms.DateInput(
                attrs={'id': 'datetimepicker_es'}
            ),
            'order_date': forms.DateInput(
                attrs={'id': 'datetimepicker_es'}
            ),

        }

    def __init__(self, *args, **kwargs):
        super(ProductCreateForm, self).__init__(*args, **kwargs)
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

class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('deadline', 'order_date', 'client', 'work_state', 'start_date', 'name', 'product_category', 'selling_price', 'note', 'photo')
        widgets = {
            'deadline': forms.DateInput(
                attrs={'id': 'datetimepicker_es'}
            ),
            'order_date': forms.DateInput(
                attrs={'id': 'datetimepicker_es'}
            ),
            'start_date': forms.DateInput(
                attrs={'id': 'datetimepicker_es'}
            ),

        }

    def __init__(self, *args, **kwargs):
        super(ProductUpdateForm, self).__init__(*args, **kwargs)
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





class ProductCategoryCreateForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super(ProductCategoryCreateForm, self).__init__(*args, **kwargs)
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


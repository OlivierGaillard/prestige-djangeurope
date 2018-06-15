from crispy_forms.helper import FormHelper
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from crispy_forms.bootstrap import TabHolder, Tab, FormActions
from crispy_forms.layout import Submit, Layout, Fieldset, Field
from django import forms
from .models import Product, ProductCategory, Order


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'product_category', 'selling_price', 'note', 'photo')

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
        fields = ('name', 'product_category', 'selling_price', 'note', 'photo')
        widgets = {
            'deadline': forms.DateInput(
                attrs={'id': 'datetimepicker_deadline'}
            ),
            'order_date': forms.DateInput(
                attrs={'id': 'datetimepicker_order'}
            ),
            'start_date': forms.DateInput(
                attrs={'id': 'datetimepicker_start_date'}
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

class ProductCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super(ProductCategoryUpdateForm, self).__init__(*args, **kwargs)
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


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('client', 'product', 'order_date', 'deadline', 'start_date', 'order_state')
        widgets = {
            'deadline': forms.DateInput(
                attrs={'id': 'datetimepicker_deadline'}
            ),
            'order_date': forms.DateInput(
                attrs={'id': 'datetimepicker_order'}
            ),
            'start_date': forms.DateInput(
                attrs={'id': 'datetimepicker_start_date'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(OrderCreateForm, self).__init__(*args, **kwargs)
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

class OrderUpdateForm(forms.ModelForm):
    generate_selling = forms.ChoiceField(widget=forms.RadioSelect(attrs={'checked': 'checked'}),
                                         choices=(('YES', _('YES')), ('NO', _('NO'))), label=_('generate_selling')
                                         )
    class Meta:
        model = Order
        fields = ('client', 'product', 'order_date', 'deadline', 'start_date', 'order_state')
        widgets = {
            'deadline': forms.DateInput(
                attrs={'id': 'datetimepicker_deadline'}
            ),
            'order_date': forms.DateInput(
                attrs={'id': 'datetimepicker_order'}
            ),
            'start_date': forms.DateInput(
                attrs={'id': 'datetimepicker_start_date'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(OrderUpdateForm, self).__init__(*args, **kwargs)
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

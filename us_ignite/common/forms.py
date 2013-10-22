from django import forms


class OrderForm(forms.Form):
    order = forms.ChoiceField(choices=())

    def __init__(self, *args, **kwargs):
        order_choices = kwargs.pop('order_choices', ())
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['order'].choices = order_choices

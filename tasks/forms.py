from django import forms
from tasks.models import Category, Event, Participant

class StyleFormMixin:
    default_class = "border to-black shadow-sm focus:border-x-black focus:ring-black rounded-2xl w-full text-center "
    default_style = "border: 1px solid black; text-align: center;   padding: 10px; text-align: center"
    default_margin = "border: 1px solid black; margin:10px text-align: center"

    def applyStyle(self):
        for key, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class' : self.default_class,
                    'placeholder' : f'Enter {field.label.lower()}',
                    'style' : self.default_style
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class' : self.default_class,
                    'placeholder' : f"Enter {field.label.lower()}",
                    'style': self.default_style
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class' : self.default_class,
                    'placeholder' : f"Enter {field.label.lower()}",
                    'style': self.default_style
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class' : "m-2",
                    'placeholder' : f"Enter {field.label.lower()}",
                    'style': self.default_style
                })


# ata holo basic...ata janar
# class EventForm(forms.Form):    
#     name = forms.CharField(max_length=200, label="Event Name")
#     description = forms.CharField(widget=forms.Textarea, label="Event Details")
#     date = forms.DateField(widget=forms.SelectDateWidget, label="Event Date")
#     location = forms.CharField(max_length=150, label="Event Location")
#     category = forms.ModelChoiceField(queryset=Category.objects.all(), label="Category")

#     def __init__(self, *args, **kwargs):
#         cat = kwargs.pop("cat", None)
#         super().__init__(*args, **kwargs)
#         if cat is not None:
#             self.fields['category'].queryset = cat

# class CategoryForm(forms.Form):
#     name = forms.CharField(max_length=100, label="Category Name")
#     description = forms.CharField(widget=forms.Textarea, label="Category Details")

# class Participant(forms.Form):
#     name = forms.CharField(max_length=100, label="Participate")
#     email = forms.EmailField(widget=forms.EmailInput, label='E-mail Address' )
#     event = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=False, label="Event")

#     def __init__(self, *args, **kwargs):
#         ev = kwargs.pop("ev", [])
#         super().__init__(*args, **kwargs)
#         self.fields['event'].choices = [
#             (even.id, even.name) for even in ev
#         ]


# this is great. ata besi besi use korbo
class EventModelForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name','description','date','location','category','status']
        widgets = {
            'date' : forms.SelectDateWidget,
            'category' : forms.RadioSelect
        }
        labels = {
            'name': 'Name',
            'description': 'Description',
            'date': 'Date',
            'location': 'Location',
            'category' : 'Category',
            'status' : 'Status'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.order_by('name')
        self.applyStyle()

class CategoryModelForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name","description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.applyStyle()

class ParticipantModelForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Participant
        fields = ["name","email","event"]

        widgets = {
            'email' : forms.EmailInput,
            'event' : forms.CheckboxSelectMultiple
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.applyStyle()





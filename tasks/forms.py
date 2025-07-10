from django import forms
from tasks.models import Category, Event, Speaker
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()


class StyleFormMixin:
    default_class = "border to-gray shadow-sm border-gray focus:border-gray focus:ring-black rounded-xl w-80 m-2 text-center "
    default_style = "text-align: center;  padding: 10px; text-align: center;"
    default_margin = "margin:10px; text-align: center"

    def applyStyle(self):
        for key, field in self.fields.items():
            label = field.label if field.label else "Field"
            label_lower = label.lower()

            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class' : self.default_class,
                    'placeholder' : f'Enter {label_lower}',
                    'style' : self.default_style
                })
            elif isinstance(field.widget, forms.EmailInput):
                field.widget.attrs.update({
                    'class' : self.default_class,
                    'placeholder' : f'Enter {label_lower}',
                    'style' : self.default_style
                })
            elif isinstance(field.widget, forms.EmailField):
                field.widget.attrs.update({
                    'class' : self.default_class,
                    'placeholder' : f'Enter {label_lower}',
                    'style' : self.default_style
                })
            elif isinstance(field.widget, forms.PasswordInput):
                field.widget.attrs.update({
                    'class' : self.default_class,
                    'placeholder' : f'{label_lower}',
                    'style' : self.default_style
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class' : self.default_class,
                    'placeholder' : f"Enter {label_lower}",
                    'style': self.default_style
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    # 'class' : self.default_class,
                    'placeholder' : f"Enter {label_lower}",
                    
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class' : "m-2",
                    'placeholder' : f"Enter {label_lower}",
                    'style': self.default_style
                })

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.applyStyle()

# this is great. ata besi besi use korbo
class EventModelForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name','description','date','location','category','status', 'asset', 'participants']
        widgets = {
            'name' : forms.TextInput(attrs={'required' : True}),
            'description' : forms.Textarea(attrs={'required' : True}),        
            'date' : forms.SelectDateWidget(attrs={'required' : True}),
            'location' : forms.TextInput(attrs={'required' : True}),
            'category' : forms.RadioSelect(attrs={'required' : True}),
            'status' : forms.Select(attrs={'required' : True}),
            # 'asset' : forms.ClearableFileInput(attrs={'required' : True}),
            'participants' : forms.CheckboxSelectMultiple()
        }
        labels = {
            'name': 'Name',
            'description': 'Description',
            'date': 'Date',
            'location': 'Location',
            'category' : 'Category',
            'status' : 'Status',
            'participants' : 'Participants'
        }   

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.order_by('name')
        self.fields['participants'].queryset = User.objects.order_by('first_name')
        self.applyStyle()

class CategoryModelForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name","description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.applyStyle()

class ParticipantModelForm(StyleFormMixin, forms.ModelForm):
    
    event = forms.ModelChoiceField(
        queryset= Event.objects.all(),
        widget= forms.Select(),
        required=True
    )

    participants = forms.ModelMultipleChoiceField(
        queryset= User.objects.all(),
        widget= forms.CheckboxSelectMultiple(),
        required=True
    )
    class Meta:
        model = Event
        fields = ["participants"]

        # widgets = {
        #     'email' : forms.EmailInput,
        # }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.applyStyle()   

        # self.fields['username'].help_text = None

class SpeakerForm(StyleFormMixin, forms.ModelForm):
    class Meta: 
        model = Speaker
        fields = ['name', 'title', 'image']
        




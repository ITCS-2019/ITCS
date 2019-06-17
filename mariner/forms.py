from django import forms

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from accounts.models import Profile
#from django.contrib.admin.widgets import FilteredSelectMultiple

#from bootstrap_datepicker_plus import DatePickerInput
#from django.contrib.admin.widgets import AdminDateWidget

from regulations.models import RegulationDoc
from mariner.models import Sailor, TrainigOrganisation, TrainigDirections, Certificate

import re
import datetime
#from datetime import timedelta

# If you don't do this you cannot use Bootstrap CSS
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30, 
                               widget=forms.TextInput(attrs={'type': 'text', 'placeholder': 'Username'}))
    password = forms.CharField(label="Password", max_length=30, 
                               widget=forms.TextInput(attrs={'type': 'password', 'placeholder': 'Password'}))


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('organization_name',)
        labels = {'organization_name': 'Назва Організації',}

class RegulationForm(forms.ModelForm):
    class Meta:
        model = RegulationDoc
        fields = (
            'date_activation', 
            'number', 
            'title', 
            'status', 
            'text', 
            'pdf_file', 
            'prev_version',  
            'organisation', 
            'regulation_organization_link',
        )

class SailorForm(forms.ModelForm):
    class Meta:
        model = Sailor
        fields = (
            'first_name_en',
            'last_name_en',
            'last_name_ukr',
            'first_name_ukr',
            'second_name_ukr',
            'born',
#            'died',
            'inn',
        )
        labels = {
            'first_name_en': 'First Name',
            'last_name_en': 'Surname',
            'last_name_ukr': 'Прiзвище',
            'first_name_ukr': 'Iм\'я',
            'second_name_ukr': 'По батькові',
            'born': 'Дата народження',
            #'died': 'Дата смертi',
            'inn': 'ІПН',
        }
        widgets = {
            'first_name_en': forms.TextInput(attrs={'placeholder': 'Ім\'я англійскою. Наприклад: \"Tan Zung\"',}),
            'last_name_en': forms.TextInput(attrs={'placeholder': 'Прізвище англійскою. Наприклад: \"Saltykov-Shchedrin\"',}),
            'last_name_ukr': forms.TextInput(attrs={'placeholder': 'Прізвище українською. Наприклад: \"Салтиков-Щедрін\"',}),
            'first_name_ukr': forms.TextInput(attrs={'placeholder': 'Ім\'я українською. Наприклад: \"Тан Зунг\"',}),
            'second_name_ukr': forms.TextInput(attrs={'placeholder': 'По батькові українською. Наприклад: \"Іванович\"',}),
            'born' : forms.DateInput(format="%d.%m.%Y", attrs={'placeholder': 'дд.мм.рррр',}),
#            'died' : forms.DateInput(format="%d.%m.%Y", attrs={'placeholder': 'дд.мм.рррр',}),
            'inn': forms.TextInput(attrs={'type': 'text', 'data-mask': '9999999999', 'placeholder': 'ІПН',}),
        }
    def clean(self):
        super(SailorForm, self).clean()
        firstNameEn = self.cleaned_data.get('first_name_en')
        lastNameEn = self.cleaned_data.get('last_name_en')
        lastNameUkr = self.cleaned_data.get('last_name_ukr')
        firstNameUkr = self.cleaned_data.get('first_name_ukr')
        secondNameUkr = self.cleaned_data.get('second_name_ukr')
        sialorBirthday = self.cleaned_data.get('born')
        dateMin = datetime.datetime.now().date() - datetime.timedelta(days=15*365)
        dateMax = datetime.datetime.now().date() - datetime.timedelta(days=100*365)
        if firstNameEn != None:
            if not bool(re.fullmatch('[a-zA-Z\-\'\s]{2,32}( [a-zA-Z\-\'\s]{2,32})?', firstNameEn)):
                self._errors['first_name_en'] = self.error_class([
                    'Помилка. Поле First Name повинно бути на латиниці. Якщо це кілька слів вони повинні бути розділені пропуском або дефісом. Наприклад: "Tan Zung"'])
        if lastNameEn != None:
            if not bool(re.fullmatch('[a-zA-Z\-\'\s]{2,32}( [a-zA-Z\-\'\s]{2,32})?', lastNameEn)):
                self._errors['last_name_en'] = self.error_class([
                    'Помилка. Поле Surname повинно бути на латиниці. Якщо це кілька слів вони повинні бути розділені пропуском або дефісом. Наприклад: "Saltykov-Shchedrin"'])
        if lastNameUkr != None:
            if not bool(re.fullmatch('[а-щА-ЩЬьЮюЯяЇїІіЄєҐґ\-\'\s]{2,32}( [а-щА-ЩЬьЮюЯяЇїІіЄєҐґ\-\'\s]{2,32})?', lastNameUkr)):
                self._errors['last_name_ukr'] = self.error_class([
                    'Помилка. Поле Прізвище повинно бути українською мовою. Якщо це кілька слів вони повинні бути розділені пропуском або дефісом. Наприклад: "Saltykov-Shchedrin"'])
        if firstNameUkr != None:
            if not bool(re.fullmatch('[а-щА-ЩЬьЮюЯяЇїІіЄєҐґ\-\'\s]{2,32}( [а-щА-ЩЬьЮюЯяЇїІіЄєҐґ\-\'\s]{2,32})?', firstNameUkr)):
                self._errors['first_name_ukr'] = self.error_class([
                    'Помилка. Поле Ім\'я повинно бути українською мовою. Якщо це кілька слів вони повинні бути розділені пропуском або дефісом. Наприклад: "Тан Зунг"'])
        if secondNameUkr != None:
            if secondNameUkr != '':
                if not bool(re.fullmatch('[а-щА-ЩЬьЮюЯяЇїІіЄєҐґ\-\'\s]{2,32}( [а-щА-ЩЬьЮюЯяЇїІіЄєҐґ\-\'\s]{2,32})?', secondNameUkr)):
                    self._errors['second_name_ukr'] = self.error_class([
                    'Помилка. Поле По батькові повинно бути українською мовою. Якщо це кілька слів вони повинні бути розділені пропуском або дефісом. Наприклад: "Санта Марія"'])
        if sialorBirthday != None:
            if sialorBirthday > dateMin:
                self._errors['born'] = self.error_class([
                    'Неприпустима дата'])
            if sialorBirthday < dateMax:
                self._errors['born'] = self.error_class([
                    'Неприпустима дата'])
                
        return self.cleaned_data

class TrainigOrganisationForm(forms.ModelForm):
    class Meta:
        model = TrainigOrganisation
        fields = (
            'organisation_id',
            'organisation_name',
            'orgnisation_email',
            'activated',
            'active_till',
            'directions',
        )
        labels = {
            'organisation_id': 'Код НТЗ',
            'organisation_name': 'Назва НТЗ',
            'orgnisation_email': 'email',
            'activated': 'Дата активації',
            'active_till': 'Дійсний до',
            'directions': 'Напрямки підготовки',
        }
        widgets = {
            'activated' : forms.DateInput(format="%d.%m.%Y", attrs={'placeholder': 'дд.мм.рррр',}),
            'active_till' : forms.DateInput(format="%d.%m.%Y", attrs={'placeholder': 'дд.мм.рррр',}),
        }


class TrainigDirectionsForm(forms.ModelForm):
    class Meta:
        model = TrainigDirections
        fields = (
            'price_id',
            'direction_title',
            'level',
            'allow_functions',
            #'price',
        )
        labels = {
            'price_id': 'Код підготовки',
            'direction_title': 'Напрямок навчання',
            'level': 'Рівень кваліфікації',
            'allow_functions': 'Дозволені рівні функцій',
            #'price': 'Цiна',
        }
        widgets = {
            'price_id' : forms.TextInput(),
            #'price': forms.TextInput(),
        }


NTZ_STATUSES = (
    (0, 'Чернетка'),
    (1, 'Обробка')
)

class CertificationForm(forms.ModelForm):
    #status = forms.ChoiceField(choices=get_status_choices())
    def __init__(self, user, statusIndex, *args, **kwargs):
        super(CertificationForm, self).__init__(*args, **kwargs)
        self.fields['training_direction'].empty_label = None
        self.fields['ntz_number'].widget.attrs['readonly'] = True
        if user.groups.all()[0].name == 'НТЗ':
            try:
                trainigOrganisation = TrainigOrganisation.objects.get(organisation_name=user.profile.organization_name)
            except TrainigOrganisation.DoesNotExist:
                user = None
            if user != None:
                if statusIndex != 2:
                    self.fields['status'] = forms.ChoiceField(choices=NTZ_STATUSES)
                    self.fields['status'].label = 'Статус'
                self.fields['training_direction'].queryset = trainigOrganisation.directions.all()
                
        if statusIndex == 1:
            self.fields['first_name_en'].widget.attrs['readonly'] = True
            self.fields['last_name_en'].widget.attrs['readonly'] = True
            self.fields['last_name_ukr'].widget.attrs['readonly'] = True
            self.fields['first_name_ukr'].widget.attrs['readonly'] = True
            self.fields['second_name_ukr'].widget.attrs['readonly'] = True
            self.fields['born'].widget.attrs['readonly'] = True
            self.fields['inn'].widget.attrs['readonly'] = True
            self.fields['date_of_issue'].widget.attrs['readonly'] = True
            self.fields['valid_date'].widget.attrs['readonly'] = True
            #self.fields['training_direction'].widget = forms.widgets.TextInput(attrs={'type': 'text',})
            self.fields['training_direction'].widget.attrs['readonly'] = True
            #self.fields['trainigOrganisation'].widget = forms.widgets.TextInput(attrs={'type': 'text',})
            self.fields['trainigOrganisation'].widget.attrs['readonly'] = True
            if user.groups.all()[0].name == 'НТЗ':
                self.fields['certf_number'].widget.attrs['readonly'] = True
            self.fields['form_number'].widget.attrs['readonly'] = True
        if statusIndex == 2:
            self.fields['first_name_en'].widget.attrs['readonly'] = True
            self.fields['last_name_en'].widget.attrs['readonly'] = True
            self.fields['last_name_ukr'].widget.attrs['readonly'] = True
            self.fields['first_name_ukr'].widget.attrs['readonly'] = True
            self.fields['second_name_ukr'].widget.attrs['readonly'] = True
            self.fields['born'].widget.attrs['readonly'] = True
            self.fields['inn'].widget.attrs['readonly'] = True
            self.fields['date_of_issue'].widget.attrs['readonly'] = True
            self.fields['valid_date'].widget.attrs['readonly'] = True
            #self.fields['training_direction'].widget = forms.widgets.TextInput(attrs={'type': 'text',})
            self.fields['training_direction'].widget.attrs['readonly'] = True
            #self.fields['trainigOrganisation'].widget = forms.widgets.TextInput(attrs={'type': 'text',})
            self.fields['trainigOrganisation'].widget.attrs['readonly'] = True
            self.fields['certf_number'].widget.attrs['readonly'] = True
            self.fields['form_number'].widget.attrs['readonly'] = True
            if user.groups.all()[0].name != 'НТЗ':
                self.fields['status'].widget.attrs['readonly'] = True


    class Meta:
        model = Certificate
        fields = (
            'first_name_en',
            'last_name_en',
            'last_name_ukr',
            'first_name_ukr',
            'second_name_ukr',
            'born',
            'inn',
            'date_of_issue',
            'valid_date',
            # 'direction_level',
            # 'direction_allow_functions',
            'training_direction',
            'trainigOrganisation',
            'form_number',
            'certf_number',
            'ntz_number',
            'status',
        )
        labels = {
            'first_name_en': 'First Name',
            'last_name_en': 'Surname',
            'last_name_ukr': 'Прiзвище',
            'first_name_ukr': 'Iм\'я',
            'second_name_ukr': 'По батькові',
            'born': 'Дата народження',
            'inn': 'ІПН',
            'date_of_issue': 'Дата видачі',
            'valid_date': 'Дійсний до',
            # 'direction_level': 'Рівень кваліфікації',
            # 'direction_allow_functions': 'Дозволені рівні функцій',
            'training_direction': 'Напрямок підготовки',
            'trainigOrganisation': 'НТЗ',
            'form_number': 'Номер бланку документу',
            'certf_number': 'Номер сертифікату',
            'ntz_number': 'Номер сертифікату НТЗ',
            'ntz_number': 'Номер сертифікату НТЗ',
            'status': 'Статус',
        }
        # >L<??????????????
        widgets = {
            'first_name_en': forms.TextInput(attrs={'placeholder': 'Ім\'я англійскою. Наприклад: \"Tan Zung\"',}),
            'last_name_en': forms.TextInput(attrs={'placeholder': 'Прізвище англійскою. Наприклад: \"Saltykov-Shchedrin\"',}),
            'last_name_ukr': forms.TextInput(attrs={'placeholder': 'Прізвище українською. Наприклад: \"Салтиков-Щедрін\"',}),
            'first_name_ukr': forms.TextInput(attrs={'placeholder': 'Ім\'я українською. Наприклад: \"Тан Зунг\"',}),
            'second_name_ukr': forms.TextInput(attrs={'placeholder': 'По батькові українською. Наприклад: \"Іванович\"',}),
            'born': forms.DateInput(format="%d.%m.%Y", attrs={'placeholder': 'дд.мм.рррр',}),
            'inn': forms.TextInput(attrs={'type': 'text', 'data-mask': '9999999999', 'placeholder': 'ІПН',}),
            'date_of_issue': forms.DateInput(format="%d.%m.%Y", attrs={'placeholder': 'дд.мм.рррр',}),
            'valid_date': forms.DateInput(format="%d.%m.%Y", attrs={'placeholder': 'дд.мм.рррр',}),
        }
    def clean(self):
        super(CertificationForm, self).clean()
        firstNameEn = self.cleaned_data.get('first_name_en')
        lastNameEn = self.cleaned_data.get('last_name_en')
        lastNameUkr = self.cleaned_data.get('last_name_ukr')
        firstNameUkr = self.cleaned_data.get('first_name_ukr')
        secondNameUkr = self.cleaned_data.get('second_name_ukr')
        sialorBirthday = self.cleaned_data.get('born')
        issueDate = self.cleaned_data.get('date_of_issue')
        dateMin = datetime.datetime.now().date() - datetime.timedelta(days=15*365)
        dateMax = datetime.datetime.now().date() - datetime.timedelta(days=100*365)
        isuDateMin = datetime.datetime.now().date() - datetime.timedelta(days=7)
        isuDateMax = datetime.datetime.now().date() + datetime.timedelta(days=7)
        if firstNameEn != None:
            if not bool(re.fullmatch('[a-zA-Z\-\'\s]{2,32}( [a-zA-Z\-\'\s]{2,32})?', firstNameEn)):
                self._errors['first_name_en'] = self.error_class([
                    'Помилка. Поле First Name повинно бути на латиниці. Якщо це кілька слів вони повинні бути розділені пропуском або дефісом. Наприклад: "Tan Zung"'])
        if lastNameEn != None:
            if not bool(re.fullmatch('[a-zA-Z\-\'\s]{2,32}( [a-zA-Z\-\'\s]{2,32})?', lastNameEn)):
                self._errors['last_name_en'] = self.error_class([
                    'Помилка. Поле Surname повинно бути на латиниці. Якщо це кілька слів вони повинні бути розділені пропуском або дефісом. Наприклад: "Saltykov-Shchedrin"'])
        if lastNameUkr != None:
            if not bool(re.fullmatch('[а-щА-ЩЬьЮюЯяЇїІіЄєҐґ\-\'\s]{2,32}( [а-щА-ЩЬьЮюЯяЇїІіЄєҐґ\-\'\s]{2,32})?', lastNameUkr)):
                self._errors['last_name_ukr'] = self.error_class([
                    'Помилка. Поле Прізвище повинно бути українською мовою. Якщо це кілька слів вони повинні бути розділені пропуском або дефісом. Наприклад: "Салтиков-Щедрін"'])
        if firstNameUkr != None:
            if not bool(re.fullmatch('[а-щА-ЩЬьЮюЯяЇїІіЄєҐґ\-\'\s]{2,32}( [а-щА-ЩЬьЮюЯяЇїІіЄєҐґ\-\'\s]{2,32})?', firstNameUkr)):
                self._errors['first_name_ukr'] = self.error_class([
                    'Помилка. Поле Ім\'я повинно бути українською мовою. Якщо це кілька слів вони повинні бути розділені пропуском або дефісом. Наприклад: "Тан Зунг"'])
        if secondNameUkr != None:
            if secondNameUkr != '':
                if not bool(re.fullmatch('[а-щА-ЩЬьЮюЯяЇїІіЄєҐґ\-\'\s]{2,32}( [а-щА-ЩЬьЮюЯяЇїІіЄєҐґ\-\'\s]{2,32})?', secondNameUkr)):
                    self._errors['second_name_ukr'] = self.error_class([
                    'Помилка. Поле По батькові повинно бути українською мовою. Якщо це кілька слів вони повинні бути розділені пропуском або дефісом. Наприклад: "Санта Марія"'])
        if sialorBirthday != None:
            if sialorBirthday > dateMin:
                self._errors['born'] = self.error_class([
                    'Неприпустима дата'])
            if sialorBirthday < dateMax:
                self._errors['born'] = self.error_class([
                    'Неприпустима дата'])
        if issueDate != None:
            if issueDate < isuDateMin:
                self._errors['date_of_issue'] = self.error_class([
                    'Неприпустима дата'])
            if issueDate > isuDateMax:
                self._errors['date_of_issue'] = self.error_class([
                    'Будь ласка, перевірте.'])
        # directionTitle = self.cleaned_data.get('training_direction')
        # cert = Certificate.objects.filter(last_name_ukr=lastNameUkr, first_name_ukr=firstNameUkr, second_name_ukr=secondNameUkr, born=sialorBirthday, training_direction=directionTitle).first()
        # if cert is not None:
            # self._errors['training_direction'] = self.error_class([
            #         'Перевірте, вже існує схожий сертифікат з таким напрямком'])
        return self.cleaned_data

class CertificationFormPDF(forms.Form):
    startDate = forms.CharField(max_length=20)
    endDate = forms.CharField(max_length=20)

class RangeNumberForm(forms.Form):
    def __init__(self, orgId, *args, **kwargs):
        super(RangeNumberForm, self).__init__(*args, **kwargs)
        exist = True
        try:
            trainigOrganisation = TrainigOrganisation.objects.get(id=orgId)
        except TrainigOrganisation.DoesNotExist:
            exist = False
        if(exist):
            ntzDirections= [(direction.pk, direction) for direction in trainigOrganisation.directions.all()]
            self.fields['directions'] = forms.ChoiceField(choices=ntzDirections)
            self.fields['directions'].label = 'Напрямки'

    directions=forms.ChoiceField()
    rangeStart = forms.CharField(label='Початок діапазону')
    rangeEnd = forms.CharField(label='Кінець діапазону')

    

class UploadXLSForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(UploadXLSForm, self).__init__(*args, **kwargs)
        if user.groups.all()[0].name == 'НТЗ':
            try:
                trainigOrganisation = TrainigOrganisation.objects.get(organisation_name=user.profile.organization_name)
            except TrainigOrganisation.DoesNotExist:
                user = None
            if user != None:
                #self.fields['directions'].queryset = trainigOrganisation.directions.all()
                DIRS = (
                (0, 'Авто визначення'))

                ntzDirections= [(direction.pk, direction) for direction in trainigOrganisation.directions.all()]
                ntzDirections.insert(0, [0, 'Авто визначення'])#([0, 'Авто визначення'])
                #DIRS.append(ntzDirections)
                self.fields['directions'] = forms.ChoiceField(choices=ntzDirections)
                self.fields['directions'].label = 'Напрямки'
        else:
            DIRS = (
                (0, 'Авто визначення'),
            )
            self.fields['directions'].label = 'Напрямки'
            self.fields['directions'] = forms.ChoiceField(choices=DIRS)

    directions=forms.ChoiceField()#(label='Напрямки', choices=DIRS)
    file = forms.FileField(label='Файл')

class CreateUserForm(forms.Form):
    userName = forms.CharField(label='Никнейм')
    userPass = forms.CharField(label='Пароль')
    userMail = forms.CharField(label='email')
    userFirstName = forms.CharField(label='Ім\'я')
    userSurname = forms.CharField(label='Прізвище')
    userGroup = forms.CharField(label='Тип групи')
    userNTZName = forms.CharField(label='Назва НТЗ')
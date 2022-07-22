from django import forms


class LicenseRequirement(forms.Form):
    number_of_medical_doctor = forms.IntegerField(required=False)
    number_of_nurse = forms.IntegerField(required=False)
    number_of_midwife = forms.IntegerField(required=False)
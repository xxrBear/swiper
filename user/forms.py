from django import forms

from user.models import User, Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nickname', 'gender', 'birthday', 'location']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

    def clean_max_distance(self):
        """自定义数据清洗最匹配距离"""
        clean_data = super().clean()
        if clean_data['max_distance'] >= clean_data['min_distance']:
            return clean_data['max_distance']
        else:
            raise forms.ValidationError('最大匹配距离不能小于最小匹配距离')

    def clean_max_dating_age(self):
        """自定义数据清洗最匹配距离"""
        clean_data = super().clean()
        if clean_data['max_dating_age'] >= clean_data['min_dating_age']:
            return clean_data['max_dating_age']
        else:
            raise forms.ValidationError('最大匹配年龄不能小于最小匹配年龄')
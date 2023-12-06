from django import forms
from django.contrib.auth.models import User
from blog.models import Profile, Question, Tag
from django.contrib.auth import hashers

class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        required=False,
        widget=forms.TextInput(
            attrs={'required': True}
        )
    )
    password = forms.CharField(
        label="Password",
        min_length=8,
        required=False,
        widget=forms.PasswordInput(
            attrs={'required': True}
        )
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("No user with such username")
        if len(username) < 2:
            raise forms.ValidationError("Username is too short")
        return username

    def clean_password(self):
        password = self.cleaned_data['password']

        if len(password) < 8:
            raise forms.ValidationError("Password length must be > 8")
        return password


class SignupForm(forms.Form):
    email = forms.EmailField(
        required=False,
        label="Email",
        widget=forms.TextInput(
            attrs={'required': True}
        )
    )
    username = forms.CharField(
        required=False,
        label="Username",
        max_length=150,
        widget=forms.TextInput(
            attrs={'required': True}
        )
    )
    password = forms.CharField(
        required=False,
        label="Password",
        min_length=8,
        max_length=128,
        widget=forms.PasswordInput(
            attrs={'required': True}
        )
    )
    repeated = forms.CharField(
        required=False,
        label="Repeat password",
        min_length=8,
        max_length=128,
        widget=forms.PasswordInput(
            attrs={'required': True}
        )
    )
    avatar = forms.ImageField(
        required=False,
        label="Upload avatar",
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
                "type": "file",
                "id": "formFile",
                "enctype": "multipart/form-data",
            }
        )
    )

    def clean(self):
        print("CLEAN DATA:", self.cleaned_data)

        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        repeated_password = self.cleaned_data['repeated']

        if len(username) < 4:
            raise forms.ValidationError("Username lenght must be > 4")
        
        if len(password) < 8:
            raise forms.ValidationError("Password length must be > 8")
        
        if password != repeated_password:
            raise forms.ValidationError("Passwords don't match")
        
        try:
            User.objects.get(username=username)
            raise forms.ValidationError("No user with such username")
        except User.DoesNotExist:
            pass
        
        return password
    
    def save(self, username, email, password):
        super().clean()

        new_user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=hashers.make_password(self.cleaned_data['password'])
        )
        Profile.objects.create(user=new_user)


class SettingsForm(forms.Form):
    email = forms.CharField(
        label="Email",
        required=False,
        widget=forms.TextInput(
            attrs={
                'required': True,
                'type': 'email',
            },
        ),
    )
    username = forms.CharField(
        label="Username",
        required=False,
        widget=forms.TextInput(
            attrs={
                'required': True,
                'min-length': 3,
            }
        )
    )
    avatar = forms.FileField(
        label="Upload avatar",
        required=False,
        widget=forms.FileInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    def clean_email(self):
        email = self.cleaned_data['email']

        if len(email) < 5:
            raise forms.ValidationError("Email length must be more than 4")
        if '@' not in email:
            raise forms.ValidationError("Invalid email!")
        if User.objects.filter(email=email).count >= 1:
            raise forms.ValidationError("Such email is already in use")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']

        if len(username) < 3:
            raise forms.ValidationError("Username length must be more than 2")
        if User.objects.filter(email=username).count >= 1:
            raise forms.ValidationError("Such username is already in use")
        return username

class AskForm(forms.Form):
    title = forms.CharField(
        label="Title",
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'title-input',
                'placeholder': 'In a nutshell',
                'required': True,
                'min-length': 11,
                'max-length': 100,
            },
        ),
    )
    description = forms.CharField(
        label="Text",
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'text-input textarea-input',
                'type': 'text',
                'placeholder': 'Describe in details',
                'max-length': 1000,
            }
        )
    )
    tags = forms.CharField(
        label="Tags",
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'tags-input',
                'placeholder': 'List tags by comma',
                'max-length': 100,
            }
        )
    )

    def clean_title(self):
        title = self.cleaned_data['title']

        if len(title) < 10:
            raise forms.ValidationError("Title length must be more than 10")
        if len(title) >= 100:
            raise forms.ValidationError("Title length must be less than 100")
        if Question.objects.get(title=title) != None:
                forms.ValidationError("Such question already exists")
        return title


    def clean_description(self):
        description = self.cleaned_data['description']
        if len(description) > 0:
            if Question.objects.gete(description=description) != None:
                forms.ValidationError("Such question already exists")
        return description


    def clean_tags(self):
        tags = self.cleaned_data['tags']

        tag_list = list()
        if len(tags) != 0:
            raw_tags = tags.split(',')
            for tag in raw_tags:
                tag_list.append(tag.strip(" "))

            for i, tag in enumerate(tag_list):
                if tag in tag_list[:i] + tag_list[i + 1:]:
                    raise forms.ValidationError(f"Tags '{tag}' is not unique")
                if len(tag) > 32:
                    raise forms.ValidationError("Tag len must be lower than 33")
                
                for c in tag:
                    if not c.isalpha():
                        raise forms.ValidationError("Tags should contain only alpha symbols")
        return tags

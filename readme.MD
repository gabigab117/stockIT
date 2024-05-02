# Enterprise Stock Manager

This Django project is a comprehensive stock management system for businesses currently under development.

This Django project is a comprehensive stock management system for businesses. It allows users to sign up, create and
manage their companies, as well as efficiently manage their stocks, goods entries, inventories, and promotions.

## Main Features

**To view the full range of functionalities, not all features are accessible directly from the main branch. Some
functionalities are located within specific branches, allowing for a more organized and manageable development process.
**

User Account Management: Users can sign up, log in, and manage their user accounts.

Multi-Enterprise Management: Users can register and manage multiple companies from their user account.

Stock Management: Companies can track and manage their product stocks. They can add new products, update stock
quantities, etc.

Goods Entry Management: Users can record goods entries into the system, specifying details such as quantity, unit price,
etc.

Inventory Management: Companies can conduct regular inventories to check stock levels and update data accordingly.

Promotion Management: Companies can create and manage promotions for their products, specifying discounts, start and end
dates, etc.

## Current Status

### Accessing Features

### Register a company

Additionally, when a user registers their company, they are automatically assigned the role of administrator. This is
facilitated by a custom permission created for this purpose.

```python
# models.py
class Company(models.Model):
    # fields here

    class Meta:
        verbose_name = "Entreprise"
        permissions = [
            ("company_admin_status", "User has all the rights on company"),
        ]
```

```python
# func package
def add_company_admin_permission(user):
    content_type = ContentType.objects.get_for_model(Company)
    permissions = Permission.objects.filter(content_type=content_type)
    for perm in permissions:
        if perm.codename == "company_admin_status":
            user.user_permissions.add(perm)
```

### SelectCompanyForm

To access the features of the system, users are required to log in to their accounts. Upon logging in, users must select
the company in which they are registered. The selection process is streamlined to display only the companies in which
the user is registered. This functionality is achieved by overriding the class constructor of the SelectCompanyForm
form.
This functionality is implemented using Django's request.session to store the user's company choice.

```py
# forms.py
class SelectCompanyForm(forms.Form):

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'] = forms.ModelChoiceField(queryset=Company.objects.filter(users=user), label="Entreprise")
```

```py
# views.py
@login_required
def select_company_view(request):
    user = request.user
    if request.method == "POST":
        form = SelectCompanyForm(user, request.POST)
        if form.is_valid():
            company = form.cleaned_data["company"]
            request.session["company"] = f"{company.name} id {company.identification}"
            messages.add_message(request, messages.INFO, f"Choix {company} validé.")
            return redirect(request.path)
    else:
        form = SelectCompanyForm(user)
    return render(request, "account/select_company.html", context={"form": form})
```

### Custom the context processor

Furthermore, the context processor has been modified to display the name of the selected company, ensuring a more
personalized user experience.

```python
# context_processor.py
def add_session_company_to_context(request):
    return {"company_session": request.session.get("company", None)}
```

```python
# settings.py
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'account.context_processors.add_session_company_to_context',
            ],
        },
    },
]
```

### Custom decorator

Moreover, a custom view decorator has been crafted to add specific functionality to views, enhancing the flexibility and
control over user interactions within the application.

```python
def company_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get("company"):
            return redirect("account:select-company")
        response = view_func(request, *args, **kwargs)
        return response

    return wrapper
```

# Pytest

Furthermore, tests are being implemented progressively alongside the development of each branch, ensuring the robustness
and reliability of the system's functionalities.

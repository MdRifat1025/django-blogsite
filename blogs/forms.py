from django import forms
from .models import Blog, Rating, Category


class BlogForm(forms.ModelForm):
    """Form for creating and editing blogs"""
    
    class Meta:
        model = Blog
        fields = ['title', 'body', 'category', 'image', 'created_at']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter blog title'
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Write your blog content here...'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'created_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }, format='%Y-%m-%dT%H:%M'),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make created_at optional
        self.fields['created_at'].required = False


class RatingForm(forms.ModelForm):
    """Form for rating blogs"""
    
    RATING_CHOICES = [(i, str(i)) for i in range(7)]
    
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Rate this blog (0-6)'
    )
    
    class Meta:
        model = Rating
        fields = ['rating', 'review']
        widgets = {
            'review': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your review (optional)...'
            }),
        }


class BlogSearchForm(forms.Form):
    """Form for searching and filtering blogs"""
    
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search blogs...'
        })
    )
    
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label='All Categories',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    author = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Author username'
        })
    )
    
    sort_by = forms.ChoiceField(
        choices=[
            ('date', 'Date (Newest First)'),
            ('-date', 'Date (Oldest First)'),
            ('rating', 'Rating (Highest First)'),
            ('-rating', 'Rating (Lowest First)'),
            ('views', 'Most Viewed'),
        ],
        required=False,
        initial='date',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

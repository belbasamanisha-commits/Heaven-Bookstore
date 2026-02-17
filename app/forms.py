from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FloatField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, NumberRange
from app.models import User


class RegistrationForm(FlaskForm):
    """User registration form"""
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=80, message='Username must be between 3 and 80 characters')
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message='Invalid email address')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message='Password must be at least 6 characters')
    ])
    password2 = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        """Check if username already exists"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different one.')
    
    def validate_email(self, email):
        """Check if email already exists"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different one.')


class LoginForm(FlaskForm):
    """User login form"""
    username = StringField('Username or Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class BookForm(FlaskForm):
    """Book management form for admin"""
    title = StringField('Title', validators=[
        DataRequired(),
        Length(max=200)
    ])
    author = StringField('Author', validators=[
        DataRequired(),
        Length(max=150)
    ])
    price_npr = FloatField('Price (NPR)', validators=[
        DataRequired(),
        NumberRange(min=0, message='Price must be positive')
    ])
    category = SelectField('Category', validators=[DataRequired()], choices=[
        ('Photography', 'Photography'),
        ('Investing', 'Investing'),
        ('Literature', 'Literature'),
        ('Languages', 'Languages'),
        ('Biography', 'Biography'),
        ('Reference', 'Reference'),
        ('Wellness', 'Wellness'),
        ('Graphic Novels', 'Graphic Novels')
    ])
    description = TextAreaField('Description', validators=[Length(max=2000)])
    image_url = StringField('Image URL', validators=[Length(max=500)])
    stock_quantity = IntegerField('Stock Quantity', validators=[
        DataRequired(),
        NumberRange(min=0, message='Stock cannot be negative')
    ])
    submit = SubmitField('Save Book')


class ReviewForm(FlaskForm):
    """Book review form"""
    rating = SelectField('Rating', validators=[DataRequired()], 
                        choices=[(str(i), f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)],
                        coerce=str)
    review_text = TextAreaField('Review', validators=[Length(max=1000)])
    submit = SubmitField('Submit Review')

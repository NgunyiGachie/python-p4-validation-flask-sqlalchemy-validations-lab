from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Author must have a name.")
        
        existing_name = Author.query.filter_by(name=name).first()
        if existing_name:
            raise ValueError("Author with {existing_name} alredy exists.")
        
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if len(phone_number) != 10 or not phone_number.isdigit():
            raise ValueError("Phone numbers must be exactly ten digits.")
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    summary = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('content', 'summary', 'category', 'title')
    def validate_post(self, key, value):
        if key == 'content' and len(value) < 250:
            raise ValueError("Post content must be at least 250 characters long.")
        if key == 'category' and value not in ["fiction", "non-fiction"]:
            raise ValueError("Category must be either 'fiction' or 'non-fiction'.")
        if key == 'summary' and len(value) > 250:
            raise ValueError("Summary must be a maximum of 250 characters long.")
        if key == 'title':
            allowed_titles = ["Won't believe", "Secret", "Top", "Guess"]
            if not any(phrase in value for phrase in allowed_titles):
                raise ValueError(f"Title must contain one of the following: {allowed_titles}")
        return value

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title}, content={self.content}, summary={self.summary})'

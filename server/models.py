from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    @validates("name")
    def validate_name(self, key, new_name):
        existing_name = Author.query.filter_by(name=new_name).first()
        if not new_name or existing_name:
            raise ValueError("Need a name and name must be unique")
        return new_name

    @validates("phone_number")
    def validate_phone_number(self, key, number):
        if number is None or len(number) != 10:
            raise ValueError("Phone number be 10 digits.")
        return number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates("title")
    def validate_title(self, key, new_title):
        if not new_title:
            raise ValueError("All posts need a title.")
        elif not "Won't Believe" or "Secret" or "Top" or "Guess" in new_title:
            raise ValueError("You need more clickbait.")
            # buzzwords = ["Won't Believe", "Secret", "Top", "Guess"]
            # if not any(buzzword in new_title for buzzword in buzzwords):
        return new_title
    
    @validates("content")
    def validate_content(self, key, content_value):
        if len(content_value) < 250:
            raise ValueError("Post content must be at least 250 characters.")
        return content_value
    
    @validates("summary")
    def validate_summary(self, key, summary_value):
        if len(summary_value) > 249:
            raise ValueError("Post summary cannot be more than 249 characters.")
        return summary_value
    
    @validates("category")
    def validate_category(self, key, category_value):
        if category_value != "Fiction" and category_value != "Non-Fiction":
            raise ValueError("Category must be Fiction or Non-Fiction")
        return category_value

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'

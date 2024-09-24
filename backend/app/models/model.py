import os

from sqlalchemy import Column, String, Text, DateTime, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship

from backend.app.core.db import Base


RecipesIngredients = Table(
    'recipe_ingredients',
    Base.metadata,
    Column('ingredient_id',Integer, ForeignKey('ingredient.id'), nullable=False, primary_key=True),
    Column('recipe_id', Integer, ForeignKey('recipe.id'), nullable=False, primary_key=True),
    Column('amount', Integer, nullable=False),
    Column('measure', String(20), nullable=False),
)

RecipesTags = Table(
    'recipe_ingredients',
    Base.metadata,
    Column('recipe_id', Integer, ForeignKey('recipe.id'), nullable=False, primary_key=True),
    Column('tag_id', Integer, ForeignKey('tag.id'), nullable=False, primary_key=True)
)

class Ingredient(Base):
    name = Column(String(100), unique=True, nullable=False)
    # устонавливаю двух сторонюю связь между моделями связанными ManyToMany
    # back_populates указывает какое поле с одной стороны связи соответствует полю с другой стороны
    recipes = relationship('Recipe', secondary=RecipesIngredients, back_populates='ingredients')


class Tag(Base):
    name = Column(String(100), unique=True, nullable=False)
    color = Column(String(7), unique=True, nullable=False)
    slug = Column(String(100), default="#ffffff",  unique=True, nullable=False)
    recipes = relationship('Recipe', secondary=RecipesTags, back_populates='tag')


class Recipe(Base):
    name = Column(String(100), unique=True, nullable=False)
    image = Column(String(100), unique=True)
    description = Column(Text, nullable=False)
    ingredients = relationship('Ingredient', secondary=RecipesIngredients, back_populates='recipes')
    tag = relationship('Tag', secondary=RecipesTags, back_populates='recipes')
    cooking_time = Column(DateTime, nullable=False)


    def get_image_url(self):
        # Вернуть URL изображения для отображения, если изображения хранятся в публичной директории
        return os.path.join('/static/uploads/', self.image_path)


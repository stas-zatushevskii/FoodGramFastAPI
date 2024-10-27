
import os
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, String, Text, DateTime, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Annotated

from app.core.db import Base  # noqa


RecipesIngredients = Table(
    'recipe_ingredients',
    Base.metadata,
    Column('ingredient_id',Integer, ForeignKey('ingredient.id'), nullable=False, primary_key=True),
    Column('recipe_id', Integer, ForeignKey('recipe.id'), nullable=False, primary_key=True),
    Column('amount', Integer, nullable=False),
)

RecipesTags = Table(
    'recipe_tags',
    Base.metadata,
    Column('recipe_id', Integer, ForeignKey('recipe.id'), nullable=False, primary_key=True),
    Column('tag_id', Integer, ForeignKey('tag.id'), nullable=False, primary_key=True)
)

class Ingredient(Base):
    name = Column(String(100), nullable=False)
    # устанавливаю двух сторонюю связь между моделями связанными ManyToMany
    # back_populates указывает какое поле с одной стороны связи соответствует полю с другой стороны
    recipes = relationship('Recipe', secondary=RecipesIngredients, back_populates='ingredients')
    measurement_unit = Column(String(20), nullable=False)


class Tag(Base):
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    color: Mapped[str] = mapped_column(unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(default="#ffffff",  unique=True, nullable=False)
    recipes = relationship('Recipe', secondary=RecipesTags, back_populates='tags')


class Recipe(Base):
    # Добавляем поле - внешний ключ пользователя.
    # User OneToMany -> Recipe
    author: Mapped[int] = mapped_column(ForeignKey('user.id'))
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    image: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(nullable=False)
    ingredients = relationship('Ingredient', secondary=RecipesIngredients, back_populates='recipes')
    tags = relationship('Tag', secondary=RecipesTags, back_populates='recipes')
    cooking_time: Mapped[datetime] = mapped_column(nullable=False)


    def get_image_url(self):
        # Вернуть URL изображения для отображения, если изображения хранятся в публичной директории
        return os.path.join('/static/uploads/', self.image_path)


class ShoppingList(Base):
    user: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    recipe: Mapped[int] = mapped_column(ForeignKey('recipe.id'), nullable=False)


class Favorite(Base):
    user: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    recipe: Mapped[int] = mapped_column(ForeignKey('recipe.id'), nullable=False)

import os

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base  # noqa

"""RecipesIngredients = Table(
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
)"""


class RecipesIngredients(Base):
    __tablename__ = "recipes_ingredients"
    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipe.id", ondelete="CASCADE"),
        primary_key=True,
    )
    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey("ingredient.id", ondelete="CASCADE"),
        primary_key=True,
    )
    amount: Mapped[int] = mapped_column(nullable=False)


class RecipesTags(Base):
    __tablename__ = "recipes_tags"
    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipe.id", ondelete="CASCADE"),
        primary_key=True,
    )
    tag_id: Mapped[int] = mapped_column(
        ForeignKey("tag.id", ondelete="CASCADE"),
        primary_key=True,
    )


class Ingredient(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name = Column(String(100), nullable=False)
    # устанавливаю двух сторонюю связь между моделями связанными ManyToMany
    # back_populates указывает какое поле с одной стороны связи соответствует полю с другой стороны
    recipes: Mapped[list["Recipe"]] = relationship(
        secondary="recipes_ingredients", back_populates="ingredients"
    )
    measurement_unit = Column(String(20), nullable=False)


class Tag(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    color: Mapped[str] = mapped_column(unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(default="#ffffff", unique=True, nullable=False)
    recipes: Mapped[list["Recipe"]] = relationship(
        secondary="recipes_tags", back_populates="tags"
    )


class Recipe(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    # Добавляем поле - внешний ключ пользователя.
    # User OneToMany -> Recipe
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    author = relationship("User", back_populates="recipes")
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    image: Mapped[str] = mapped_column()
    text: Mapped[str] = mapped_column(nullable=False)
    ingredients: Mapped[list["Ingredient"]] = relationship(
        back_populates="recipes", secondary="recipes_ingredients"
    )
    tags: Mapped[list["Tag"]] = relationship(
        back_populates="recipes", secondary="recipes_tags"
    )
    cooking_time: Mapped[int] = mapped_column(nullable=False)

    def get_image_url(self):
        # Вернуть URL изображения для отображения, если изображения хранятся в публичной директории
        return os.path.join("/static/uploads/", self.image_path)


class ShoppingList(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    recipe: Mapped[int] = mapped_column(ForeignKey("recipe.id"), nullable=False)


class Favorite(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    recipe: Mapped[int] = mapped_column(ForeignKey("recipe.id"), nullable=False)

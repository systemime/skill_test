from django.db import models


class Topping(models.Model):
    name = models.CharField(max_length=30)


class Pizza(models.Model):
    name = models.CharField(max_length=50)
    toppings = models.ManyToManyField(Topping)

    def __str__(self):
        return "{} ({})".format(
            self.name,
            ", ".join(topping.name for topping in self.toppings.all()),
        )


class Country(models.Model):
    """城市"""

    name = models.CharField(max_length=100)
    is_remove = models.BooleanField(default=False)


class Author(models.Model):
    """作者"""

    name = models.CharField(max_length=100)
    city = models.ForeignKey(
        Country,
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        related_name="author",
    )


class Book(models.Model):
    """书籍"""

    name = models.CharField(max_length=100)
    author = models.ForeignKey(
        Author,
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        related_name="book",
    )


class Bookk(models.Model):
    title = models.CharField(max_length=100)
    author = models.ManyToManyField(Author)

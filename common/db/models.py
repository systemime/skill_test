"""
关于django_mysql这个库，想办法看看能不能替换调
"""
from django.conf import settings
from django.db import models
from django.db.models import DateTimeField
from django.utils import timezone
from django_mysql.models import QuerySetMixin as DMQuerySetMixin
from hashid_field.field import HashidFieldMixin


class BaseHashidFieldMixin(HashidFieldMixin):
    def __init__(
        self,
        *args,
        salt=settings.HASHID_FIELD_SALT,
        min_length=settings.HASHID_FIELD_MIN_LENGTH,
        alphabet=settings.HASHID_ALPHABETS,
        allow_int_lookup=settings.HASHID_FIELD_ALLOW_INT_LOOKUP,
        **kwargs,
    ):
        self.salt = salt
        self.min_length = min_length
        self.alphabet = alphabet
        self.allow_int_lookup = allow_int_lookup
        super().__init__(
            salt=self.salt,
            min_length=self.min_length,
            alphabet=self.alphabet,
            allow_int_lookup=self.allow_int_lookup,
            *args,
            **kwargs,
        )

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs.pop("salt", None)
        kwargs.pop("min_length", None)
        kwargs.pop("alphabet", None)
        kwargs.pop("allow_int_lookup", None)
        return name, path, args, kwargs


class BaseHashidAutoField(BaseHashidFieldMixin, models.BigAutoField):
    description = "A Hashids obscured BigAutoField"


class BaseQuerySet(DMQuerySetMixin, models.QuerySet):
    def delete(self, soft=True):  # pylint: disable=arguments-differ
        if soft:
            return self.update(is_removed=True)
        return super().delete()


class BaseManager(models.Manager):
    _queryset_class = BaseQuerySet

    def get_queryset(self):
        """
        Return queryset limited to not removed entries.
        """
        kwargs = {"model": self.model, "using": self._db}
        if hasattr(self, "_hints"):
            kwargs["hints"] = self._hints

        return self._queryset_class(**kwargs).filter(is_removed=False)


class BaseModel(models.Model):
    id = BaseHashidAutoField(primary_key=True)
    create_time = DateTimeField("创建时间", editable=False)
    update_time = DateTimeField("更新时间", editable=False, null=True)
    is_removed = models.BooleanField("软删字段，表示是否已被删除", default=False, editable=False)

    objects = BaseManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def delete(
        self, using=None, soft=True, *args, **kwargs
    ):  # pylint: disable=arguments-differ, keyword-arg-before-vararg
        if soft:
            self.is_removed = True
            self.save(using=using)
        else:
            super().delete(using=using, *args, **kwargs)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        now = timezone.localtime()
        if not self.id:
            self.create_time = now
            self.update_time = None
        else:
            self.update_time = now
        return super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )

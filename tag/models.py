from django.db import models

# Create your models here.
class TagModelManager(models.Manager):

    def get_or_create_or_update(self, code, description):
        try:
            tag = super().get(code=code)

            if tag.description != description:
                tag.description = description
                tag.save()

            return tag
        except Tag.DoesNotExist:
            tag = Tag(code=code, description=description)
            tag.save()
            return tag


class Tag(models.Model):
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=500)

    objects = TagModelManager()

    def __str__(self):
        return self.description
 
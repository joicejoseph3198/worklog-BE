from django.db import models
# Create your models here.
class Task(models.Model):
    user_id = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    tag = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField()
    # audit fields
    active = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"Task(user_id={self.user_id}, "
            f"title={self.title}, "
            f"description={self.description}, "
            f"tag={self.tag}, "
            f"date={self.date} "
            f"active={self.active}, "
            f"deleted={self.deleted}, "
            f"created_at={self.created_at}, "
            f"updated_at={self.updated_at})"
    )
    # To explicitly set properties
    class Meta:
        db_table = "task"
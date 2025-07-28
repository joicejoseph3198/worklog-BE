from django.db import models

# Create your models here.
class Task(models.Model):
    STATUS_CHOICES = [
        ('not-started', 'Not Started'),
        ('in-progress', 'In Progress'),
        ('blocked', 'Blocked'),
        ('done', 'Done'),
        ('rollover', 'Rollover'),
        ('initiated', 'Initiated'),
    ]
    
    user_id = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    tag = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField()
    ticked = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='not-started'
    )
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
            f"date={self.date}, "
            f"ticked={self.ticked}, "
            f"status={self.status}, "
            f"active={self.active}, "
            f"deleted={self.deleted}, "
            f"created_at={self.created_at}, "
            f"updated_at={self.updated_at})"
        )
    
    # To explicitly set properties
    class Meta:
        db_table = "task"

class Notes(models.Model):
    user_id = models.CharField(max_length=100)
    date = models.DateField()
    body = models.TextField(blank=True, max_length=20000)
    # audit fields
    active = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Note(id={self.id}, user={self.user_id}, date={self.date})"

    class Meta:
        db_table = "notes"
        unique_together = ['user_id', 'date']


class Schedule(models.Model):
    user_id = models.CharField(max_length=100)
    date = models.DateField()
    hour = models.IntegerField()
    detail = models.TextField(blank=True, max_length=500)
    # audit fields
    active = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Schedule(id={self.id}, user={self.user_id}, date={self.date} hour={self.hour} detail={self.detail})"

    class Meta:
        db_table = "schedule"

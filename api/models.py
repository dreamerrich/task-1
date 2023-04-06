from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import User

language = (('react', 'REACT'), ('python', 'PYTHON'), ('node', 'NODE'),('angular', 'ANGULAR'))

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, password=None, password2=None):
        if not username:
            raise ValueError('Users must have a name')
        user = self.model(
            username=self.normalize_email(username),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password=None,password2=None):
        user = self.create_user(
            username=username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
    )
    FCM = models.CharField(max_length=255, null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=255,unique=True,null=True)
    objects = UserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):  
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin

class Project(models.Model):
    UUID = models.CharField(primary_key=True, max_length=10)
    project_name = models.CharField(max_length=70, unique=True)
    description = models.CharField(max_length=255)
    project_color_identify = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.UUID)

class taskAsinee(models.Model):
    name = models.CharField(max_length=255)
    language = models.CharField(max_length=255,default='react', choices=language)

    def __str__(self):
        return str(self.name)

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    assign_to = models.ForeignKey(taskAsinee, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Permission(models.Model):
    name = models.ForeignKey(taskAsinee, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)

    class Meta:
        permissions = [
            ("view_project", "Can view project"),
        ]
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import User

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
        
        return self.is_admin

    def has_module_perms(self, app_label):
        
        return True
    @property
    def is_staff(self):
        
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

class Task(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    task_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    assign_to = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.project)
    
    def __str__(self):
        return str(self.id)
    

class Permission(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    can_edit = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    can_create = models.BooleanField(default=False)
    project = models.ForeignKey(Task, on_delete=models.CASCADE, default="create")
    
    def __str__(self):
        return str(self.project)
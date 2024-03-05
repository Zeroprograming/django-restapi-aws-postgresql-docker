from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, Permission

class UserType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class User(AbstractUser):

    username = None
    email = models.EmailField(unique=True)  # Usar el email como único campo
    type = models.ForeignKey(UserType,
                             on_delete=models.CASCADE, null=False)
    
    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set')    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    @staticmethod
    def get_all_users():
        return User.objects.all()
    
    def save(self, *args, **kwargs):
        # Antes de guardar el usuario, encriptamos la contraseña si no está encriptada
        if not self.password.startswith('bcrypt_sha256'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)



import uuid
from django.db import models,IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from apps.connection.models import Follow
from django.core.exceptions import ValidationError


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **kwargs):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            **kwargs
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(unique=True,default=uuid.uuid4,editable=False)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField(null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100,blank=True,null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    profile_picture = models.ImageField(upload_to='img/profile', blank=True, null=True)
    bio = models.CharField(max_length=512, blank=True, null=True)
    private_account = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','first_name', 'age']

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def _get_user_with_list_id(self,ids):
        return User.objects.filter(id__in=ids)
    @property
    def followers_real(self):
        return self._get_user_with_list_id(self.followers.filter(in_request=False).values_list('following',flat=True))

    @property
    def followings_real(self):
        return self._get_user_with_list_id(self.followings.filter(in_request=False).values_list('follower',flat=True))

    @property
    def followers_in_reqest(self):
        return self._get_user_with_list_id(self.followers.filter(in_request=True).values_list('following',flat=True))

    @property
    def followings_in_reuest(self):
        return self._get_user_with_list_id(self.followings.filter(in_request=True).values_list('follower',flat=True))

    def follow(self,username):
        try:
            target_user = User.objects.get(username=username)
            is_privet = target_user.private_account
            Follow.objects.create(following=self, follower=target_user, in_request=is_privet)
            if is_privet:
                msg = f"Sended Request Following for {target_user}"
            else:
                msg = f"You Followings {target_user}"
            return True, msg
        except IntegrityError as e:
            return False, str(e)
        except ValidationError as e:
            return False, e
        except ObjectDoesNotExist:
            return False, f"user with username '{username}' doe's not exist."

    def unfollow(self,username):
        try:
            try:
                target_user = User.objects.get(username=username)
            except ObjectDoesNotExist:
                return False, "User Does Not Exist."
            follow_obj = Follow.objects.get(following=self, follower=target_user)
            if follow_obj.in_request:
                msg = f"Removed Request Follow {target_user}"
            else:
                msg = f"You Unfollowed {target_user}"
            follow_obj.delete()
            return True, msg
        except ObjectDoesNotExist:
            return False, f"You don't following {username}."


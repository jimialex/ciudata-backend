# -*- coding: utf-8 -*-

from apps.accounts.models import User
from django.contrib.auth.models import Group


class UserService:
    """Contains all utility methods to help user precesses."""

    @classmethod
    def update_profile(cls, user, changes):
        """Updates some fields of the user instance."""
        group = changes.pop('groups', None)

        if 'username' in changes:
            user.username = changes.get('username')

        if 'first_name' in changes:
            user.first_name = changes.get('first_name')

        if 'last_name' in changes:
            user.last_name = changes.get('last_name')

        if 'photo' in changes:
            if changes.get('photo') is not None:
                _photo = changes.get('photo')
                user.photo.save(_photo.name, _photo)

        if type(group) != list:
            groups = [Group.objects.get(pk=group.id)]
            user.groups.set(groups)
        else:
            user.groups.set(group)

        user.save()
        user.refresh_from_db()

        return user

    @classmethod
    def register_new_user(cls, user_data, is_active=False):
        """Creates an user instance."""
        plain_password = user_data.pop('password')
        group = user_data.pop('groups', None)

        if 'username' not in user_data and 'email' in user_data:
            user_data['username'] = user_data['email']

        user = User(**user_data)
        user.is_active = is_active
        user.set_password(plain_password)
        user.save()

        if type(group) != list:
            groups = [Group.objects.get(pk=group.id)]
            user.groups.set(groups)
        else:
            user.groups.set(group)

        return user

    @classmethod
    def create_or_update_for_social_networks(cls, email, first_name, last_name):
        user, created = User.objects.update_or_create(
            email=email, defaults={
                'first_name': first_name,
                'last_name': last_name,
                'is_active': True,
            }
        )
        user.save()

        return user

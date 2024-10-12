from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from .models import Customer

class UserService:
    def create_user(self, username: str, password: str) -> User:
        """
        Create a new user.

        Args:
            username (str): The username of the new user.
            password (str): The password of the new user.

        Returns:
            User: The newly created user object.
        """
        # Create the user with the provided username and hashed password
        user = User.objects.create(username=username, password=make_password(password))
        # Save the user to the database
        user.save()
        return user

    def add_user_to_group(self, user: User, group_name: str):
        """
        Add a user to a specific group.

        Args:
            user (User): The user to add to the group.
            group_name (str): The name of the group.

        Returns:
            None
        """
        # Get or create the group with the provided name
        group, created = Group.objects.get_or_create(name=group_name)
        # Add the user to the group
        user.groups.add(group)

class CustomerService:
    def create_customer(self, user: User, website: str) -> Customer:
        """
        Create a new customer.

        Args:
            user (User): The user associated with the customer.
            website (str): The website of the customer.

        Returns:
            Customer: The newly created customer object.
        """
        # Create the customer with the provided user and website
        return Customer.objects.create(user=user, website=website)

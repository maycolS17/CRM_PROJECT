from django.core.management.base import BaseCommand
from core.models import User, Company, Customer, Interaction
from faker import Faker
import random
from datetime import timedelta

class Command(BaseCommand):
    help = "popula la base de datos con datos de prueba"

    def handle(selft, *args, **kwargs):
        fake = Faker()

        selft.stdout.write("creando usuarios...")
        users = []
        for _ in range(3):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password="admin123"
            )
            users.append(user)

        selft.stdout.write("creando compañias...")
        companies = [Company.objects.create(name=fake.company()) for _ in range(20)]

        selft.stdout.write("creando clientes...")
        customers = []
        for _ in range(1000):
            customers.append(Customer.objects.create(
                name=fake.name(),
                birthday=fake.date_of_birth(minimum_age=10, maximum_age=70),
                company=random.choice(companies),
                representative=random.choice(users)
            ))

        selft.stdout.write("creando interacciones...")
        interaction_types = ['call', 'email', 'SMS', 'Facebook']
        batch_size = 2
        total_customers = len(customers)

        for index, customer in enumerate(customers):
            for _ in range(batch_size):
                Interaction.objects.create(
                    customer=customer,
                    interaction_type=random.choice(interaction_types),
                    timestamp=fake.date_time_this_year()
                )
            if (index +1) % 100 == 0:
                selft.stdout.write(f"clientes procesados: {index+1}/{total_customers}")

        selft.stdout.write(selft.style.SUCCESS("Datos creados exitosamente"))

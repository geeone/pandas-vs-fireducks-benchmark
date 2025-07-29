from datetime import datetime, timedelta
import random

from faker import Faker

import numpy as np
import pandas as pd


faker = Faker()
rows = 10000000

print("Generating dataset with 10M+ rows... this may take a few minutes")


def generate_random_date():
    start_date = datetime(2015, 1, 1)
    end_date = datetime.today()
    return start_date + timedelta(days=random.randint(0, (end_date - start_date).days))


data = {
    "id": np.arange(1, rows + 1),
    "name": [faker.name() for _ in range(rows)],
    "email": [faker.email() for _ in range(rows)],
    "age": np.random.randint(18, 80, size=rows),
    "income": np.round(np.random.normal(50000, 20000, size=rows), 2),
    "signup_date": [generate_random_date().strftime('%Y-%m-%d') for _ in range(rows)],
    "country": [faker.country() for _ in range(rows)],
    "is_active": np.random.choice([True, False], size=rows),
    "feedback": [faker.paragraph(nb_sentences=3) for _ in range(rows)]
}

df = pd.DataFrame(data)
df.to_csv("synthetic_data.csv", index=False)

print("Done. Dataset saved as synthetic_data.csv")

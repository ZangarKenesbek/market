import os
import pickle
import pandas as pd
from sklearn.linear_model import LinearRegression
from django.conf import settings
from django.core.management.base import BaseCommand
from products.ml_utils import get_order_data

class Command(BaseCommand):
    help = 'Train separate ML models per product based on order data'

    def handle(self, *args, **kwargs):
        df = get_order_data()
        df['date'] = pd.to_datetime(df['date'])
        df['day'] = df['date'].dt.dayofyear

        models_dir = os.path.join(settings.BASE_DIR, 'ml_models')
        os.makedirs(models_dir, exist_ok=True)

        for product_id, group in df.groupby('product_id'):
            X = group[['day']]
            y = group['quantity']

            if len(X) < 2:
                self.stdout.write(f'Skipping product {product_id}: not enough data.')
                continue

            model = LinearRegression()
            model.fit(X, y)

            model_path = os.path.join(models_dir, f'model_{product_id}.pkl')
            with open(model_path, 'wb') as f:
                pickle.dump(model, f)

            self.stdout.write(self.style.SUCCESS(f'Model saved for product {product_id} → {model_path}'))

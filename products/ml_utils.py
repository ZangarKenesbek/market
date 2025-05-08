import pandas as pd
from products.models import OrderItem

def get_order_data():
    items = OrderItem.objects.select_related('product')
    data = []
    for item in items:
        data.append({
            'product_id': item.product.id,
            'product_name': item.product.name,
            'quantity': item.quantity,
            'date': item.order.created_at,
        })
    return pd.DataFrame(data)

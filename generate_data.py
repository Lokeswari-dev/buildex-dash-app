import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_dummy_data(num_records=500):
    np.random.seed(42)
    random.seed(42)
    
    locations = ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Pune']
    materials = ['Cement', 'Steel', 'Bricks', 'Sand', 'Gravel', 'Wood']
    payment_statuses = ['Paid', 'Pending', 'Failed']
    
    data = []
    start_date = datetime(2025, 1, 1)
    
    for i in range(num_records):
        location = random.choice(locations)
        material = random.choice(materials)
        payment_status = np.random.choice(payment_statuses, p=[0.7, 0.2, 0.1])
        revenue = round(random.uniform(1000, 50000), 2)
        date = start_date + timedelta(days=random.randint(0, 365))
        
        data.append({
            'Order ID': f'ORD-{1000+i}',
            'Date': date.strftime('%Y-%m-%d'),
            'Location': location,
            'Material': material,
            'Revenue': revenue,
            'Payment Status': payment_status,
        })
        
    df = pd.DataFrame(data)
    df.to_csv('buildex_data.csv', index=False)
    print("buildex_data.csv generated successfully.")

if __name__ == '__main__':
    generate_dummy_data()

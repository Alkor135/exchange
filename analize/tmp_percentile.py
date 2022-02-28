import pandas as pd

edge_only = 0.1  # Задание 10% перцентиля
df = pd.DataFrame({'field_A': [139490.0, 139240.0]})

val_min = df['field_A'].quantile(edge_only)
print(val_min)

val_max = df['field_A'].quantile(1 - edge_only)
print(val_max)

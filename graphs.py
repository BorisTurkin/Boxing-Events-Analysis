import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path


PATH = str(Path(__file__).parent.absolute()) + '/'
df = pd.read_csv(PATH + 'data/pbc_events.csv')
# Generate a dataframe with unqiue names, nationality and work locations
df_1 = df[['name_1', 'nationality_1', 'work_location_1']]
df_1.columns = ['name', 'nationality', 'work_location']
df_2 = df[['name_2', 'nationality_2', 'work_location_2']]
df_2.columns = ['name', 'nationality', 'work_location']
df_names = pd.concat([df_1, df_2], axis=0).drop_duplicates()


# Weight classes distribution.
sns.countplot(
    y='weight_class',
    data=df,
    order=df['weight_class'].value_counts().index)
plt.title('Weight Classes Distribution')
plt.xlabel('frequency')
plt.show()


# Height difference distribution.
sns.distplot(
    (df['height_1'] - df['height_2']))
plt.title('Height Difference Distribution')
plt.xlabel('frequency')
plt.show()


# Plot of nationalities
sns.countplot(
    y='nationality',
    data=df_names,
    order=df_names['nationality'].value_counts().iloc[:10].index)
plt.title('Nationalities Ranked')
plt.xlabel('frequency')
plt.show()


# Plot of nationalities
sns.countplot(
    y='work_location',
    data=df_names,
    order=df_names['work_location'].value_counts().iloc[:10].index)
plt.title('Work Location Ranked')
plt.xlabel('frequency')
plt.show()

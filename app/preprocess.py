import pandas as pd
import numpy as np
from .model_loader import scaler, feature_names, age_medians, fare_99th, fare_quantiles

def prepare_features(raw_data: dict) -> np.ndarray:
    df = pd.DataFrame([raw_data])
    data = df.copy()

    # 1. Удаление ненужных столбцов
    data.drop(columns=['PassengerId', 'Ticket', 'Cabin'], inplace=True, errors='ignore')

    # 2. Пол
    data['Sex'] = data['Sex'].map({'male': 0, 'female': 1})

    # 3. Порт посадки
    data['Embarked'] = data['Embarked'].fillna('S')

    # 4. Возраст 
    def fill_age(row):
        if pd.isnull(row['Age']):
            return age_medians.get(row['Pclass'], 28.0)
        return row['Age']
    data['Age'] = data.apply(fill_age, axis=1)

    # 5. Winsorize Fare
    data['Fare'] = data['Fare'].apply(lambda x: min(x, fare_99th))

    # 6. Title
    data['Title'] = data['Name'].str.extract(r' ([A-Za-z]+)\.', expand=False)
    title_mapping = {
        'Mr': 'Mr', 'Miss': 'Miss', 'Mrs': 'Mrs', 'Master': 'Master',
        'Dr': 'Rare', 'Rev': 'Rare', 'Col': 'Rare', 'Major': 'Rare',
        'Mlle': 'Rare', 'Ms': 'Rare', 'Mme': 'Rare', 'Don': 'Rare',
        'Lady': 'Rare', 'Sir': 'Rare', 'Capt': 'Rare', 'Countess': 'Rare',
        'Jonkheer': 'Rare'
    }
    data['Title'] = data['Title'].map(title_mapping).fillna('Rare')

    # 7. AgeGroup
    data['AgeGroup'] = pd.cut(data['Age'], bins=[0,12,19,60,100], labels=['Child','Teen','Adult','Senior'])

    # 8. Дополнительные признаки
    data['MinorAge'] = (data['Age'] < 18).astype(int)
    data['FamilySize'] = data['SibSp'] + data['Parch'] + 1
    data['IsAlone'] = (data['FamilySize'] == 1).astype(int)

    # 9. FareGroup по квантилям
    def assign_fare_group(fare):
        if fare <= fare_quantiles[0]:
            return 'Low'
        elif fare <= fare_quantiles[1]:
            return 'Medium'
        elif fare <= fare_quantiles[2]:
            return 'High'
        else:
            return 'VeryHigh'
    data['FareGroup'] = data['Fare'].apply(assign_fare_group)

    # 10. Удаление Name
    data.drop(columns=['Name'], inplace=True, errors='ignore')

    # 11. One‑Hot Encoding
    categorical_features = ['Embarked', 'Title', 'AgeGroup', 'FareGroup']
    data = pd.get_dummies(data, columns=categorical_features, drop_first=True)
    bool_cols = data.select_dtypes(include='bool').columns
    data[bool_cols] = data[bool_cols].astype(int)

    # 12. Колонки к порядку feature_names
    for col in feature_names:
        if col not in data.columns:
            data[col] = 0
    data = data[feature_names]

    # 13. Масштабирование числовых признаков
    numeric_features = ['Age', 'Fare', 'FamilySize', 'SibSp', 'Parch', 'Pclass']
    data[numeric_features] = scaler.transform(data[numeric_features])

    return data.values
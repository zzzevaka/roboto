# data preprocessing utils
import numpy as np
from sklearn import preprocessing


def transform_datetime_index_to_values(df, values=('weekday', 'day', 'month', 'hour')):
    """
    Получает DataFrame, у которого индекс - datetime.
    Возвращает DataFrame с добавленными значениями(по-умолчанию: день недели, месяца, номер месяца, час)
    """
    new_df = df.copy()

    def get_value_from_datetime(dt, value):
        attr = getattr(dt, value)
        return attr() if callable(attr) else attr

    for value in values:
        new_df[value] = new_df.index.map(lambda x: get_value_from_datetime(x, value))

    return new_df


def transform_categorial(df, categorial_columns, transformer=preprocessing.LabelBinarizer):
    """Преобразует категориальные признаки"""
    ret_df = df.copy()
    for feature in categorial_columns:
        le = transformer()
        transformed_data = le.fit_transform(df[feature])
        new_columns = ['{}_{}'.format(feature, c) for c in le.classes_]
        for i in range(len(new_columns)):
            ret_df[new_columns[i]] = transformed_data[:,i]
    return ret_df.drop(categorial_columns, axis=1)


def drop_until_first_full_field(df):
    """получает датафрейф и дропает все строки, пока не попадется полностью заполненная"""
    first_full_field_index = None
    for index, row in df.iterrows():
        if not row.isna().any():
            first_full_field_index = index
            break
    return df[first_full_field_index:]


def time_series_difference(df, difference_values, columns, shape3d=False):
    """
    Добавляет в DataFrame дифференцированные значения
    df - DataFrame
    difference_values - значения диффреренцирования
                        ([12,11,10,9,8,7,6,5,4,3,2,1] - добавит колонки за 12 интервалов)
    columns - колонки, которые требуется обработать
    shape3d - формат для рекурентных нейронных сетей
    """
    m, f = df.shape
    ret_df = None
    max_diff_value = 0
    for t in difference_values:
        new_columns = ['{}_{}'.format(c, t) for c in columns]
        tmp_df = df.drop(columns, axis=1)
        tmp_df[new_columns] = df[columns].diff(t)
        tmp_df = tmp_df.values
        if shape3d:
            tmp_df = tmp_df.reshape(m, 1, f)
        max_diff_value = max(max_diff_value, t)
        if ret_df is None:
            ret_df = tmp_df
        else:
            ret_df = np.hstack([tmp_df, ret_df])
    return ret_df[max_diff_value:]

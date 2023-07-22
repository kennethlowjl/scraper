import numpy as np
import pandas as pd
import re

# load data
cars = pd.read_csv('sg_used_cars.csv', thousands=',')

# create brand and model columns
cars['brand'] = cars['name'].apply(lambda x: x.split()[0])

def car_model(x):
    model = ' '.join(x.split()[1:])
    return model

cars['model'] = np.vectorize(car_model)(cars['name'])
cars.drop('name', axis=1, inplace=True)

# re-order columns
front_two_columns = ['brand', 'model']
cars = cars[front_two_columns + [col for col in cars if col not in front_two_columns]]

# clean up owners column
cars.rename(columns = {'owners ':'owners'}, inplace=True)
cars['owners'] = np.vectorize(lambda x: x.strip())(cars['owners'])

# flag if COE is extended
def is_coe_extended(model):
    if re.findall(r'\(.*COE.*\)', model):
        return True
    else:
        return False

cars['COE_extended'] = np.vectorize(is_coe_extended)(cars['model'])

# parse dates and calculate maturity_date
cars['reg_date'] = pd.to_datetime(cars['reg_date'])

def maturity_date(coe_extended, model, reg_date):
    if coe_extended:
        if re.findall(r'\d{2}/\d{4}', model):
            maturity_date = re.findall(r'\d{2}/\d{4}', model)[0]
        else:
            maturity_date = (pd.to_datetime(reg_date) + np.timedelta64(20, 'Y')).date()
    else:
        maturity_date = (pd.to_datetime(reg_date) + np.timedelta64(10, 'Y')).date()

    return maturity_date

cars['maturity_date'] = np.vectorize(maturity_date)(cars['COE_extended'], cars['model'], cars['reg_date'])

# remove COE information from model
def remove_coe(model):
    if re.findall(r'\(.*COE.*\)', model):
        coe = re.findall(r'\(.*COE.*\)', model)[0]
        model = model.replace(coe, '')
    return model

cars['model'] = np.vectorize(remove_coe)(cars['model'])
cars['maturity_date'] = pd.to_datetime(cars['maturity_date'])

# calculate years_left and age
def years_left(coe_extended, reg_date, maturity_date):
    years_left = (pd.to_datetime(maturity_date) - pd.to_datetime('2023-06-12')) / np.timedelta64(1, 'Y')
    return round(years_left, 1)

cars['years_left'] = np.vectorize(years_left)(cars['COE_extended'], cars['reg_date'], cars['maturity_date'])
cars['age'] = round((pd.to_datetime('2023-06-12') - cars['reg_date']) / np.timedelta64(1, 'Y'), 1)

# rearrange columns
cars = cars[['brand', 'model', 'price', 'depre', 'age', 'mileage', 'engine_cap', 'power', 'owners', 'reg_date', 'maturity_date', 'years_left', 'COE_extended']]

# clean up price
cars = cars[cars['price'] != '.A']
cars['price'] = pd.to_numeric(cars['price'].apply(lambda x: x.replace(',', '') if isinstance(x, str) else x))

# drop rows with missing depre or reg_date
cars.dropna(how='any', subset=['depre', 'reg_date'], inplace=True)

# drop duplicates
cars.drop_duplicates(inplace=True)

# save cleaned dataframe to csv
cars.to_csv('cleaned_cars.csv', index=False)

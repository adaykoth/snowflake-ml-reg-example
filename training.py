from snowflake.ml.modeling.xgboost import XGBRegressor
from snowflake.ml.registry import Registry

import pandas as pd
import numpy as np


from utils import get_session

def generate_data(session):
    np.random.seed(42)

    # Generate a DataFrame with 1000 rows and 4 columns of random floats
    num_rows = 1000
    df = pd.DataFrame(np.random.rand(num_rows, 4), columns=['a', 'b', 'c', 'd'])
    df.columns = df.columns.str.upper().str.replace(' ', '')
    # Convert the Pandas DataFrame to a Snowpark DataFrame
    snow_df = session.create_dataframe(df)
    return snow_df

def train_model(data, params):
    # Train an XGBoost model
    xgb = XGBRegressor(
        **params,
        input_cols=['A', 'B', 'C'],
        label_cols=['D'],
        output_cols=['pred_d'],
        drop_input_cols=True,
    )
    xgb.fit(data)

    return xgb

def register_model(model, data, session, name):
    model_reg = Registry(session=session,
                         database_name="core",
                         schema_name='test')

    sample_data = data.select(['A', 'B', 'C']).limit(100)

    model_reg.log_model(model,
                        model_name=name,
                        version_name='v3',
                        sample_input_data=sample_data
                        )
def main():
    params = {
        "objective": "reg:squarederror",
        "eval_metric": "rmse",
        "learning_rate": 0.1,
        "max_depth": 10,
        "n_estimators": 100,
        "max_leaves": 10,
    }
    params2 = {
        "objective": "reg:squarederror",
        "eval_metric": "rmse",
        "learning_rate": 0.1,
        "max_depth": 2,
        "n_estimators": 10,
        "max_leaves": 2,
    }
    _ = get_session.session()
    data = generate_data(_)
    model = train_model(data, params)
    model2 = train_model(data, params2)
    register_model(model, data, _, 'model1')
    register_model(model2, data, _, 'model2')


if __name__ == "__main__":
    main()
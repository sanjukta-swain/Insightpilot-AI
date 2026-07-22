import pandas as pd
from sklearn.linear_model import LinearRegression


def forecast_sales(df):
    # Convert Order Date to datetime
    df["Order Date"] = pd.to_datetime(df["Order Date"])

    # Monthly Sales
    monthly_sales = (
        df.groupby(df["Order Date"].dt.to_period("M"))["Sales"]
        .sum()
        .reset_index()
    )

    monthly_sales["Order Date"] = monthly_sales["Order Date"].astype(str)

    # Create Month Number
    monthly_sales["Month"] = range(len(monthly_sales))

    # Train Model
    X = monthly_sales[["Month"]]
    y = monthly_sales["Sales"]

    model = LinearRegression()
    model.fit(X, y)

    # Predict Next 6 Months
    future_months = pd.DataFrame({
        "Month": range(len(monthly_sales), len(monthly_sales) + 6)
    })

    predictions = model.predict(future_months)

    future_months["Predicted Sales"] = predictions

    return monthly_sales, future_months
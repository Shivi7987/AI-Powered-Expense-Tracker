

from django.shortcuts import render
import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from django.utils.timezone import now
from expenses.models import Expense
from django.contrib import messages
import matplotlib.pyplot as plt
from django.contrib.auth.decorators import login_required


@login_required(login_url='/authentication/login')
def forecast(request):
    expenses = Expense.objects.filter(owner=request.user).order_by('-date')[:30]

    if len(expenses) < 10:
        messages.error(request, "Not enough expenses to make a forecast.")
        return render(request, 'expense_forecast/index.html')

    # ✅ DataFrame banana
    data = pd.DataFrame({
        'Date': [expense.date for expense in expenses],
        'Expenses': [expense.amount for expense in expenses],
        'Category': [expense.category for expense in expenses]
    })

    # ✅ IMPORTANT FIXES
    data['Date'] = pd.to_datetime(data['Date'])   # 🔥 add this
    data['Expenses'] = pd.to_numeric(data['Expenses'], errors='coerce')
    data['Category'] = data['Category'].astype(str)
    data = data.dropna(subset=['Category', 'Expenses'])
    
    data = data.sort_values(by='Date')      # ✅ ADD THIS
    data.set_index('Date', inplace=True)# ✅ ADD THIS
    
    if data.empty:
          messages.error(request, "No valid expense data found.")
          return render(request, 'expense_forecast/index.html')

    # ✅ ARIMA
    model = ARIMA(data['Expenses'], order=(5, 1, 0))
    model_fit = model.fit()

    forecast_steps = 30
    next_day = now().date() + pd.DateOffset(days=1)
    forecast_index = pd.date_range(start=next_day, periods=forecast_steps, freq='D')

    forecast_values = model_fit.forecast(steps=forecast_steps)

    # ✅ Forecast Data
    forecast_data = pd.DataFrame({
        'Date': forecast_index,
        'Forecasted_Expenses': forecast_values
    })

    forecast_data_list = forecast_data.to_dict(orient='records')
    total_forecasted_expenses = np.sum(forecast_values)

    # ✅ SAFE CATEGORY CALCULATION (no groupby error)
    category_forecasts = {}
    for i in range(len(data)):
        cat = str(data.iloc[i]['Category'])
        amt = float(data.iloc[i]['Expenses'])

        if cat in category_forecasts:
            category_forecasts[cat] += amt
        else:
            category_forecasts[cat] = amt

    # ✅ Plot
    plt.figure(figsize=(10, 6))
    plt.plot(data.index, data['Expenses'], label='Previous Expenses')
    plt.plot(forecast_index, forecast_values, label='Forecasted Expenses')
    plt.xlabel('Date')
    plt.ylabel('Expenses')
    plt.title('Expense Forecast for Next 30 Days')
    plt.legend()

    plot_file = 'static/img/forecast_plot.png'
    plt.savefig(plot_file)
    plt.close()

    # ✅ Context
    context = {
        'forecast_data': forecast_data_list,
        'total_forecasted_expenses': total_forecasted_expenses,
        'category_forecasts': category_forecasts,
        'plot_file': plot_file
    }
    
    return render(request, 'expense_forecast/index.html', context)

  
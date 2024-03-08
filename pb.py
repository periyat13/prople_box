import pandas as pd
from datetime import datetime, timedelta

df = pd.read_csv('input.csv')


output_columns = ['Employee Code', 'Manager Employee Code', 'Last Compensation', 'Compensation',
                  'Last Pay Raise Date', 'Variable Pay', 'Tenure in Org', 'Performance Rating',
                  'Engagement Score', 'Effective Date', 'End Date']
output_df = pd.DataFrame(columns=output_columns)


def calculate_end_date(effective_date, next_effective_date):
    if pd.isnull(next_effective_date):
        return datetime(2100, 1, 1)
    return next_effective_date - timedelta(days=1)

for _, employee_data in df.iterrows():
    for i in range(1, 3):  # Assuming there are two sets of Review and Engagement data
        review_col = f'Review {i}'
        engagement_col = f'Engagement {i}'
        review_date_col = f'Review {i} date'
        engagement_date_col = f'Engagement {i} date'
        
        if not pd.isnull(employee_data[review_date_col]):
            effective_date = datetime.strptime(employee_data[review_date_col], '%Y-%m-%d')
            
            historical_row = {
                'Employee Code': employee_data['Employee Code'],
                'Manager Employee Code': employee_data['Manager Employee Code'],
                'Last Compensation': employee_data['Compensation'],
                'Compensation': employee_data[f'Compensation {i}'],
                'Last Pay Raise Date': employee_data[f'Compensation {i} date'],
                'Variable Pay': employee_data[f'Compensation {i + 1}'],
                'Tenure in Org': 0,
                'Performance Rating': employee_data[review_col],
                'Engagement Score': employee_data[engagement_col],
                'Effective Date': effective_date,
                'End Date': employee_data['Date of Exit']
            }


            output_df = output_df.append(historical_row, ignore_index=True)


output_df.sort_values(by=['Employee Code', 'Effective Date'], inplace=True) 
output_df.to_csv('file.csv', index=False)

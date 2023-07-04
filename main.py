import pandas as pd


def load_data(file_path):
    """
    Step A: Load the CSV data
    """
    return pd.read_csv(file_path)


def filter_data(data):
    """
    Step A: Filter the data based on conditions provided
    """
    # Convert quote_datetime and expiration to datetime objects
    data['quote_datetime'] = pd.to_datetime(data['quote_datetime'])
    data['expiration'] = pd.to_datetime(data['expiration'])

    # Filter rows where quote_datetime and expiration are the same date
    same_date = data['quote_datetime'].dt.date == data['expiration'].dt.date
    data = data[same_date]
    
    # Filter rows where option_type is 'C'
    data = data[data['option_type'] == 'C']

    # Filter rows where strike is greater than underlying_ask
    data = data[data['strike'] > data['underlying_ask']]
    
    return data


def calculate_combo_values(data):
    """
    Step A: Calculate combo values for sets of 3
    """
    # Sort data by strike
    data = data.sort_values(by='strike')

    # Calculate combo values
    combo_values = []
    for i in range(0, len(data) - 2, 3):
        low_ask = data.iloc[i]['ask']
        mid_bid = data.iloc[i + 1]['bid']
        high_ask = data.iloc[i + 2]['ask']
        combo_value = low_ask - 2 * mid_bid + high_ask
        combo_values.append(
            (data.iloc[i]['strike'], data.iloc[i + 1]['strike'], data.iloc[i + 2]['strike'], combo_value))

    return combo_values


def filter_combo_values(combo_values, max_value=3.3):
    """
    Step B: Filter combo values less than max_value
    """
    return [cv for cv in combo_values if cv[3] < max_value]


def save_to_csv(data, output_path):
    """
    Step C: Save the data to a CSV file
    """
    pd.DataFrame(data, columns=['Low Strike', 'Mid Strike', 'High Strike', 'Combo Value']).to_csv(output_path,
                                                                                                  index=False)


if __name__ == "__main__":
    # Use the correct file paths, the below is done for the example file.
    file_path = 'example v2.csv'
    output_path = 'output.csv'

    # Step A
    data = load_data(file_path)
    data = filter_data(data)
    combo_values = calculate_combo_values(data)

    # Step B
    filtered_combo_values = filter_combo_values(combo_values)

    # Step C
    save_to_csv(filtered_combo_values, output_path)

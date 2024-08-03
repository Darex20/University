import pandas as pd

# Function to convert integer ratings to decimal format (7 -> 7.0)
def format_ratings(rating):
    try:
        # Convert to float and check if it's a whole number
        float_rating = float(rating)
        if float_rating.is_integer():
            # Format the rating to one decimal place
            return f"{int(float_rating)}.0"
        else:
            # Return the rating as is
            return rating
    except ValueError:
        # Return the rating as is if it's not a number
        return rating

def main():
    # Replace 'path_to_your_csv_file.csv' with the path to your CSV file
    file_path = 'movies.csv'
    
    # Load the dataset
    df = pd.read_csv(file_path)
    
    # Ensure that the rating column is read as a string
    df['Rating'] = df['Rating'].astype(str)
    
    # Apply the formatting function to each rating
    df['Rating'] = df['Rating'].apply(format_ratings)
    
    # Save the updated dataframe back to a CSV file
    df.to_csv('updated_dataset.csv', index=False)

if __name__ == "__main__":
    main()

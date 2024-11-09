import os
import openai
import matplotlib.pyplot as plt

# OpenAI API key
openai.api_key = 'YOUR_API_KEY_HERE'

# Emission factor constants
GAS_EMISSION_FACTOR = 5.3  # kg CO2 per therm
GASOLINE_CAR_EMISSION_FACTOR = 2.31  # kg CO2 per mile
HYBRID_CAR_EMISSION_FACTOR = 1.6  # kg CO2 per mile
FLIGHT_EMISSION_FACTOR = 0.09  # kg CO2 per mile per passenger (approx.)
DIET_EMISSIONS = {
    'omnivore': 2.5,  # kg CO2 per day
    'vegetarian': 1.7,
    'vegan': 1.5
}
TRASH_EMISSION_FACTOR = 0.5  # kg CO2 per kg of waste
RECYCLING_SAVINGS_FACTOR = 0.2  # kg CO2 saved per kg recycled

def get_user_inputs():
    electricity_kwh = float(os.environ.get('electricity_kwh', 500)) 
    gas_usage = float(os.environ.get('gas_usage', 800))  
    gasoline_mileage = float(os.environ.get('gasoline_mileage', 12000))  
    hybrid_mileage = float(os.environ.get('hybrid_mileage', 8000))  
    num_flights = int(os.environ.get('num_flights', 2))  
    diet_type = os.environ.get('diet_type', 'omnivore')  
    trash_amount = float(os.environ.get('trash_amount', 500))  
    recycling_amount = float(os.environ.get('recycling_amount', 800))  
    return electricity_kwh, gas_usage, gasoline_mileage, hybrid_mileage, num_flights, diet_type, trash_amount, recycling_amount

def calculate_electricity_emissions(kwh):
    emission_factor = 0.92  # kg CO2 per kWh
    return kwh * emission_factor

def calculate_gas_emissions(therms):
    return therms * GAS_EMISSION_FACTOR

def calculate_transport_emissions(gasoline_miles, hybrid_miles):
    gasoline_emissions = gasoline_miles * GASOLINE_CAR_EMISSION_FACTOR
    hybrid_emissions = hybrid_miles * HYBRID_CAR_EMISSION_FACTOR
    return gasoline_emissions + hybrid_emissions

def calculate_flight_emissions(num_flights):
    avg_flight_distance = 2000  # Approx. distance per round-trip flight
    return num_flights * avg_flight_distance * FLIGHT_EMISSION_FACTOR

def calculate_diet_emissions(diet_type):
    daily_emission = DIET_EMISSIONS.get(diet_type.lower(), DIET_EMISSIONS['omnivore'])
    return daily_emission * 365  # since client wants annual

def calculate_waste_emissions(trash_kg, recycling_kg):
    trash_emissions = trash_kg * TRASH_EMISSION_FACTOR
    recycling_savings = recycling_kg * RECYCLING_SAVINGS_FACTOR
    return trash_emissions - recycling_savings

def fetch_comparisons_and_suggestions(electricity_emissions, gas_emissions, transport_emissions, flight_emissions, diet_emissions, waste_emissions):
    try:
        # Combine emissions data into a summary
        emissions_summary = f"Electricity Emissions: {electricity_emissions:.2f} kg CO2\n"
        emissions_summary += f"Gas Emissions: {gas_emissions:.2f} kg CO2\n"
        emissions_summary += f"Transport Emissions: {transport_emissions:.2f} kg CO2\n"
        emissions_summary += f"Flight Emissions: {flight_emissions:.2f} kg CO2\n"
        emissions_summary += f"Diet Emissions: {diet_emissions:.2f} kg CO2\n"
        emissions_summary += f"Waste Emissions: {waste_emissions:.2f} kg CO2\n"
        
        # Generate comparison and suggestion content using the OpenAI API
        response = openai.chat.completions.create(
            model="gpt-4o",  # Replace with the desired model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Here are the emissions data for a user:"},
                {"role": "user", "content": emissions_summary},
                {"role": "user", "content": "Please provide a well-structured report that includes the following:"},
                {"role": "user", "content": "1. Comparisons to national (USA for now) and global averages. You have to search online for the averages as user will not input them."},
                {"role": "user", "content": "2. Personalized recommendations based on the emissions data."},
                {"role": "user", "content": "Please ensure the report is formatted for easy inclusion in a report with clear headings and content. Also, your report will be read by the user directly so do not talk about the user like a 3rd person. Address them by you as you are speaking to the user directly. And, try to get your facts from this url https://css.umich.edu/publications/factsheets/sustainability-indicators/carbon-footprint-factsheet and https://ourworldindata.org/co2-emissions but if what you need is not there, you are free to check other sources. Make sure you provide both national and global data and NUMBERS."},
            ]
        )
        
        report = response.choices[0].message.content
        return report
    
    except Exception as e:
        print(f"Error fetching suggestions: {e}")
        return None, None

def generate_report(electricity_emissions, gas_emissions, transport_emissions, flight_emissions, diet_emissions, waste_emissions):
    total_emissions = sum([electricity_emissions, gas_emissions, transport_emissions, flight_emissions, diet_emissions, waste_emissions])
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)

    report_file = os.path.join(output_dir, 'report.txt')
    with open(report_file, 'w') as f:
        f.write(f"Total Annual Carbon Footprint: {total_emissions:.2f} kg CO2\n")
        
        # Fetch the well-structured report from GPT
        report = fetch_comparisons_and_suggestions(
            electricity_emissions, gas_emissions, transport_emissions, flight_emissions, diet_emissions, waste_emissions
        )

        # Write the entire report to the file
        if report:
            f.write(report)


def plot_emissions(electricity, gas, transport, flights, diet, waste):
    categories = ['Home Energy', 'Transportation', 'Air Travel', 'Food', 'Waste']
    emissions = [electricity + gas, transport, flights, diet, waste]
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)  # Ensure the output directory exists
    
    plt.figure(figsize=(8, 5))
    plt.bar(categories, emissions, color=['green', 'blue', 'red', 'orange', 'purple'])
    plt.title('Carbon Footprint by Category')
    plt.ylabel('kg CO2')
    chart_file = os.path.join(output_dir, 'emissions_chart.png')
    plt.savefig(chart_file)


# Main function to run the widget
def main():
    # Get inputs
    electricity_kwh, gas_usage, gasoline_mileage, hybrid_mileage, num_flights, diet_type, trash_amount, recycling_amount = get_user_inputs()

    # Calculate emissions
    electricity_emissions = calculate_electricity_emissions(electricity_kwh)
    gas_emissions = calculate_gas_emissions(gas_usage)
    transport_emissions = calculate_transport_emissions(gasoline_mileage, hybrid_mileage)
    flight_emissions = calculate_flight_emissions(num_flights)
    diet_emissions = calculate_diet_emissions(diet_type)
    waste_emissions = calculate_waste_emissions(trash_amount, recycling_amount)

    # Generate report and plot
    generate_report(electricity_emissions, gas_emissions, transport_emissions, flight_emissions, diet_emissions, waste_emissions)
    plot_emissions(electricity_emissions, gas_emissions, transport_emissions, flight_emissions, diet_emissions, waste_emissions)

if __name__ == "__main__":
    main()

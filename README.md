# Carbon Footprint Widget

The **Carbon Footprint Widget** is a Python-based tool designed to help households calculate their annual carbon emissions and identify practical strategies to reduce them. This widget provides insights by analyzing data inputs such as energy usage, transportation habits, diet, and waste production, generating a report that breaks down emissions by category and offers personalized reduction strategies.

## Features
- **Emissions Calculation**: Computes annual CO2 emissions based on electricity and gas usage, vehicle mileage, air travel, diet, and waste.
- **Category Breakdown**: Details emissions by source (e.g., home energy, transport, food, waste).
- **Comparative Analysis**: Shows how emissions stack up against national (USA) and global averages.
- **Actionable Recommendations**: Offers tailored suggestions for reducing emissions, such as energy-saving tips and sustainable living practices.

## Technologies Used
- **Python**: Core programming language for computation and report generation.
- **OpenAI API**: Provides personalized comparisons and recommendations.
- **Matplotlib** (optional): Generates charts for data visualization.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/lydacious/carbon-footprint-widget.git
   cd carbon-footprint-widget
   ```
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Make sure to type in your OpenAI API key in `run.py`.

2. Run the Python script and input the required data when prompted:
   ```bash
   python carbon_footprint_widget.py
   ```
3. The tool will generate a report in the `output` directory containing a breakdown of your emissions and personalized recommendations.


## Example Output
```
Total Annual Carbon Footprint: 15,000 kg CO2
Breakdown by category:
 - Home Energy: 4,700 kg CO2
 - Transportation: 7,800 kg CO2
 - Air Travel: 360 kg CO2
 - Food: 2,000 kg CO2
 - Waste: 140 kg CO2

Comparison to National and Global Averages:
[Detailed report here]

Personalized Recommendations:
- Use energy-efficient appliances.
- Reduce vehicle mileage by carpooling or using public transport.
- Incorporate more plant-based meals.
- Increase recycling efforts.
```

## License
This project is open-source and licensed under the [MIT License](LICENSE).

## Contributions
Contributions are welcome! Feel free to open an issue or submit a pull request.

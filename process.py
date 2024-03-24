import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

# Load the datasets
company_level_metrics = pd.read_csv('company_level_metrics.csv')
geographies = pd.read_csv('geographies.csv')
sectors = pd.read_csv('sectors.csv')

# Prepare geographies and sectors for merging
geographies_mapped = geographies.set_index('country')
sectors_mapped = sectors[['sector_level_3', 'sector_level_1']].drop_duplicates().set_index('sector_level_3')

# Merge the datasets
company_metrics_enriched = company_level_metrics.join(geographies_mapped, on='company_geography').join(sectors_mapped, on='sector_level_3')

# Calculate the EV/EBITDA multiples
company_metrics_enriched['ebitda_multiple_at_entry'] = company_metrics_enriched['at_entry_ev'] / company_metrics_enriched['at_entry_ebidta']
company_metrics_enriched['ebitda_multiple_at_rd'] = company_metrics_enriched['at_rd_ev'] / company_metrics_enriched['at_rd_ebidta']

# Convert 'record_date' and 'investment_date' to datetime
company_metrics_enriched['record_date'] = pd.to_datetime(company_metrics_enriched['record_date'], errors='coerce')
company_metrics_enriched['investment_date'] = pd.to_datetime(company_metrics_enriched['investment_date'], errors='coerce')

# Drop rows with missing values in 'ebitda_multiple_at_entry' and 'ebitda_multiple_at_rd'
company_metrics_cleaned = company_metrics_enriched.dropna(subset=['ebitda_multiple_at_entry', 'ebitda_multiple_at_rd'])

# Aggregating EV/EBITDA multiples by Sector Level 1 and Continent
aggregated_by_sector = company_metrics_cleaned.groupby(['sector_level_1', 'record_date'])[['ebitda_multiple_at_entry', 'ebitda_multiple_at_rd']].mean().reset_index()
aggregated_by_continent = company_metrics_cleaned.groupby(['continent', 'record_date'])[['ebitda_multiple_at_entry', 'ebitda_multiple_at_rd']].mean().reset_index()

# Visualization of EV/EBITDA Multiples Over Time by Sector and Continent
plt.figure(figsize=(16, 12))

# Time series line plot for Sectors
plt.subplot(2, 1, 1)
sns.lineplot(data=aggregated_by_sector, x='record_date', y='ebitda_multiple_at_rd', hue='sector_level_1', marker='o', palette='tab10')
plt.title('EV/EBITDA Multiples Over Time by Sector', fontsize=16)
plt.xlabel('Record Date', fontsize=14)
plt.ylabel('EV/EBITDA Multiple', fontsize=14)
plt.xticks(rotation=45)
plt.grid(True)
plt.legend(title='Sector', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.gca().xaxis.set_major_locator(mdates.YearLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

# Time series line plot for Continents
plt.subplot(2, 1, 2)
sns.lineplot(data=aggregated_by_continent, x='record_date', y='ebitda_multiple_at_rd', hue='continent', marker='o', palette='coolwarm')
plt.title('EV/EBITDA Multiples Over Time by Continent', fontsize=16)
plt.xlabel('Record Date', fontsize=14)
plt.ylabel('EV/EBITDA Multiple', fontsize=14)
plt.xticks(rotation=45)
plt.grid(True)
plt.legend(title='Continent', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.gca().xaxis.set_major_locator(mdates.YearLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

plt.tight_layout()
# plt.show()
plt.savefig('output_plot.png', dpi=300, bbox_inches='tight')
plt.show()

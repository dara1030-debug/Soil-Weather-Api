# Integrating Soil and Weather APIs

A Streamlit application for ITD112 Laboratory Exercise 1. It combines SoilGrids soil-property estimates with historical Open-Meteo weather data for selected sites in Mindanao, Philippines.

## What It Does

- Retrieves topsoil properties from SoilGrids 2.0 for each selected site.
- Retrieves historical daily weather data from Open-Meteo in a single multi-site request.
- Converts SoilGrids values using the API-provided `d_factor`.
- Joins static soil data to daily weather records by site.
- Calculates daily water balance: `precipitation_sum - et0_fao_evapotranspiration`.
- Displays six exploratory analyses and lets users download CSV results.
- Includes an optional soil-texture comparison across three depth intervals.

## Data Sources

| Source | Data used | Notes |
| --- | --- | --- |
| [ISRIC SoilGrids 2.0](https://www.isric.org/explore/soilgrids) | Clay, sand, silt, pH (`phh2o`), and soil organic carbon (`soc`) | Baseline layer: `0-5cm`; modeled estimates, licensed CC BY 4.0. |
| [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api) | Daily mean temperature, precipitation, and FAO reference ET0 | Historical daily data, licensed CC BY 4.0. |

No database or API key is required.

## Default Study Sites

| Site | Latitude | Longitude |
| --- | ---: | ---: |
| Iligan City | 8.200 | 124.300 |
| Malaybalay | 8.150 | 125.130 |
| Valencia | 7.900 | 125.090 |
| Davao (Calinan) | 7.190 | 125.460 |
| General Santos | 6.150 | 125.150 |

Users can select any subset of these sites and choose a date range in the sidebar.

## Workflow

1. Choose sites and a date range.
2. Build requests for Open-Meteo and SoilGrids.
3. Retrieve and cache API responses with retries and timeouts.
4. Parse the JSON responses into weather and soil tables.
5. Join the tables by site and calculate water balance.
6. Explore the charts and download the CSV files.

Open-Meteo accepts all selected coordinates in one request. SoilGrids accepts one point per request, so the app sends one request for each selected site. Uncached SoilGrids requests are spaced by 12 seconds as a fair-use measure.

Successful responses are stored in `cache/`. Repeating the same request can reuse the saved response instead of contacting the API again.

## Analyses

| Analysis | Question answered |
| --- | --- |
| Temperature over time | How does daily mean temperature change over time? Includes a 7-day rolling mean. |
| Rainfall and ET0 | Does rainfall meet evaporative demand? Compares monthly precipitation and reference ET0. |
| Rainfall variability | How variable is daily rainfall by month? |
| Topsoil texture | What are the relative sand, silt, and clay proportions at each site? |
| Soil and water stress | How do clay content, water balance, and soil organic carbon compare across sites? |
| Site comparison map | Where are the sites, and how do rainfall and soil organic carbon differ? |

The optional depth analysis retrieves texture data for `0-5cm`, `5-15cm`, and `15-30cm` layers for one selected site.

## Installation

1. Clone the repository and enter the project directory.

   ```bash
   git clone <repository-url>
   cd api-app
   ```

2. Create and activate a virtual environment.

   Windows PowerShell:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   macOS or Linux:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install the dependencies.

   ```bash
   pip install -r requirements.txt
   ```

4. Start the application.

   ```bash
   python -m streamlit run streamlit_app.py
   ```

Streamlit normally serves the app at `http://localhost:8501`.

## Using the App

1. Select at least one site in the sidebar.
2. Set a valid start and end date.
3. Select **Run the integration**.
4. Review the retrieved and integrated data, then explore the analyses.
5. Optionally retrieve the soil-depth profile.
6. Download the results from the Export section.

## Exports

| File | Contents |
| --- | --- |
| `site_summary.csv` | One row per selected site with summarized weather metrics and soil properties. |
| `integrated_daily.csv` | Daily weather records joined with soil properties and calculated water balance. |

Exported dates use `YYYY-MM-DD`, and numeric values are rounded to two decimal places.

## Project Structure

```text
api-app/
|- .streamlit/
|  `- config.toml       # Streamlit theme configuration
|- cache/                # Saved API responses
|- requirements.txt      # Python dependencies
|- README.md
`- streamlit_app.py      # Application, requests, processing, charts, and exports
```

## Limitations

- SoilGrids values are modeled estimates, not direct field measurements.
- Soil data may be unavailable for some coordinates, and the public SoilGrids service may be temporarily unavailable.
- Soil properties are static for each selected coordinate; weather data vary by day.
- The selected locations are a small sample of Mindanao sites.
- The soil and water-stress comparison is exploratory, especially with a small number of sites.
- Historical weather coverage depends on the chosen date range and API availability.

## Technologies

Python, Streamlit, Requests, pandas, NumPy, and Plotly.

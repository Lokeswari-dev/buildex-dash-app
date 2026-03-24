# 🏗️ Buildex India - Real-time Sales Analytics Dashboard

This is a high-performance, **interactive web dashboard** built using **Python, Dash, and Plotly**. It provides real-time insights into sales performance, revenue distribution, and payment collection risks for Buildex India.

## 🚀 Key Features
* **Live Data Updates**: Integrated with `dcc.Interval` to automatically refresh charts every 5 seconds when the backend data changes.
* **Interactive KPIs**: Real-time tracking of **Total Revenue**, **Pending Amount**, and **Total Order Count**.
* **Geographical Analysis**: Visualizing revenue across major Indian cities using grouped bar charts.
* **Payment Risk Assessment**: A dynamic Donut chart to monitor **Paid vs. Pending vs. Failed** transactions.
* **Mobile Responsive**: Built with `dash-bootstrap-components` to ensure seamless viewing on both Desktop and Mobile browsers.

## 🛠️ Tech Stack
* **Language**: Python 3.x
* **Framework**: Dash (by Plotly)
* **Data Handling**: Pandas
* **Visualization**: Plotly Express
* **Styling**: Dash Bootstrap Components
* **Deployment**: Render

## 📂 Project Structure
* `app.py`: Main Python code for the Dash app.
* `buildex_data.csv`: Dataset containing sales and payment records.
* `requirements.txt`: List of Python libraries required for the app.
* `generate_data.py`: Script used for generating/updating sample data.

## ⚙️ How to Run Locally
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python app.py`
4. Open `http://127.0.0.1:8050/` in your browser.

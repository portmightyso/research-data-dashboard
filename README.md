# Research Data Management (RDM) & Analytics Dashboard

A lightweight, customized Research Data Management (RDM) and reactive analytics dashboard prototype designed for laboratory data tracking and simulation pipelines. Built with **Django (Python)** for a secure backend API and **Vue.js + Chart.js** for a dynamic, non-reloading frontend interface.

## 🌟 Key Features

- **Project Infrastructure Management:** Centralized allocation of specific simulation runs, experimental setups, and project ownership.
- **Secure Data Logging Gateway:** Active endpoint to log runtime metrics and variables accompanied by data-quality status tags (*Success*, *Anomaly/Noise*, *Needs Retest*).
- **Reactive Analytics Pipeline:** A highly responsive frontend interface allowing researchers to dynamically search, filter datasets by quality state, and visualize parameter trends instantly using real-time charts.
- **Data Export:** Integrated one-click CSV exporter for seamless data post-processing in engineering environments like MATLAB or Python scripts.

## 🛠️ Tech Stack

- **Backend:** Python, Django, Django REST Framework (DRF)
- **Frontend:** Vue.js (CDN/Reactive Components), HTML5, CSS3
- **Data Visualization:** Chart.js
- **Database:** SQLite (Default for prototype)

## 📁 Project Structure

```text
├── research_dashboard/     # Django project configuration
├── data_logging/           # Core application logic
│   ├── models.py           # Database architecture for simulation logs
│   ├── views.py            # API views and data processing logic
│   └── urls.py             # API endpoint routing
├── templates/
│   └── index.html          # Vue.js frontend & Chart.js visualization
├── .gitignore              # Environment and cache filtering
├── manage.py
└── requirements.txt

# ⚡ Energy Insights Pipeline

A containerized data pipeline for processing, storing, and forecasting electricity load data in Germany based on Open Data. 

---

## 🧱 Architecture Overview

```
                         +---------------------+
                         |  External CSV Data  |
                         +----------+----------+
                                    |
                                    v
                       +------------+-------------+
                       |   Data Pipeline (ETL)    |
                       |   `data_pipeline/`       |
                       +------------+-------------+
                                    |
                                    v
                      +-------------+--------------+
                      |   PostgreSQL (Docker)      |
                      |   Table: `daily_load`      |
                      +-------------+--------------+
                                    |
                                    v
                       +------------+-------------+
                       |   Forecasting (Prophet)   |
                       |   `forecasting/model.py` |
                       +--------------------------+
```

---

## 🚀 Getting Started

### Prerequisites

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- Python 3.9+ with `venv` or `pyenv` (for running forecasting scripts locally)

---

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/energy-insights-pipeline.git
cd energy-insights-pipeline
```

---

### 2. Spin Up Services with Docker Compose

```bash
docker-compose up -d
```

This boots a PostgreSQL container (`energy_postgres`) exposing port `5432`.

---

### 3. Verify the Database Setup

Once the container is running:

```bash
docker exec -it energy_postgres psql -U postgres -d energy
```

Check the preloaded data:

```sql
SELECT * FROM daily_load LIMIT 10;
```

---

### 4. Forecasting with Prophet

Run the time series model to generate a forecast:

```bash
cd forecasting
python3 model.py
```

> ⚠️ Ensure the PostgreSQL hostname matches the container's internal network. If running outside Docker, use `localhost`; if from a different container, use the service name `energy_postgres`.

---

## 🛠 Configuration

### `.env` (optional)

You can define database credentials and host info in a `.env` file:

```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=energy
POSTGRES_HOST=localhost
```

---

## 📂 Project Structure

```bash
energy-insights-pipeline/
│
├── data_pipeline/           # ETL logic and data loading
├── forecasting/             # Forecast models (e.g., Prophet)
├── dashboards/              # Dashboard visualization (planned)
├── db/                      # SQL schemas or migrations
├── dags/                    # Airflow DAGs (future)
├── Dockerfile               # App-level Dockerfile (placeholder)
├── docker-compose.yml       # Container orchestration
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

---

## 🧪 Tech Stack

| Layer          | Tool                     |
|----------------|--------------------------|
| Language       | Python 3.9+              |
| Forecasting    | [Prophet](https://facebook.github.io/prophet/) |
| Database       | PostgreSQL 15 (Dockerized) |
| Container Mgmt | Docker & Docker Compose  |
| Visualization  | Plotly / Dash (optional) |

---

## 🧠 Known Issues

Warning about plotly still being unable to be imported is unrelated to the core functionality of the script.

---

## 🧭 Roadmap

- [ ] Add Airflow DAGs for orchestration
- [ ] Streamlit/Plotly Dash dashboards
- [ ] CI/CD pipeline via GitHub Actions
- [ ] Unit tests & linters (e.g., `pytest`, `flake8`)

---

## 🤝 Contributing

We welcome contributions! Please open an issue to discuss features or submit a pull request.

---

## 🪪 License

MIT License © 2025 David Manning

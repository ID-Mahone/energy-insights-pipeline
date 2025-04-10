# ⚡ Energy Insights Pipeline

A containerized data pipeline for processing, storing, and forecasting electricity load data in Germany based on Open Data. It integrates forecasting models, database management, and REST API endpoints for easy consumption of forecast results.

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
                       |   `forecasting/model.py`  |
                       +-------------+-------------+
                                    |
                                    v
                       +-----------------------------+
                       |   API Service (FastAPI)      |
                       |   `forecasting/serve.py`     |
                       +-----------------------------+
```

---

## 🚀 Getting Started

### Prerequisites

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- Python 3.9+ with `venv` or `pyenv` (for running forecasting scripts locally)
- Prophet (https://facebook.github.io/prophet/)

**Required Python Libraries:**
- `prophet`: For time-series forecasting
- `fastapi`: To serve the model via a REST API
- `uvicorn`: ASGI server to run FastAPI
- `plotly`: For interactive visualization
- `psycopg2`: For PostgreSQL database interaction
- `joblib`: For model persistence

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

This will spin up a PostgreSQL container (`energy_postgres`) exposing port `5432`.

---

### 3. Verify the Database Setup

Once the container is running, verify that the database is set up correctly:

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

### 5. Serve the Forecast with FastAPI

To start the FastAPI server and serve the forecasting model as an API:

```bash
cd forecasting
uvicorn serve:app --reload
```

This starts the FastAPI server at [http://127.0.0.1:8000](http://127.0.0.1:8000). You can now access the forecasting endpoint to make predictions.

---

## 🛠 Configuration

### `.env` (optional)

You can define database credentials and host info in a `.env` file for easy configuration:

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
| Forecasting    | Prophet                |
| Database       | PostgreSQL 15            |
| Container Mgmt | Docker & Docker Compose  |
| API            | FastAPI                  |
| Visualization  | Plotly / Dash            |

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

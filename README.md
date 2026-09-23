# Simulated Robotic Arm Monitoring System

A small simulated monitoring system built to demonstrate Python,
Linux, REST APIs and Node-RED.

This project simulates telemetry from an industrial robotic arm and makes it accessible through a REST API built with FastAPI.
Node-RED periodically retrieves the telemetry, processes it and displays the results through
a live monitoring dashboard.

Note: Although postgres is containerised, a fully containerised stack still needs to be implemented.

![Robot monitoring dashboard](screenshots/demo.gif)

## Technologies

- Python
- FastAPI
- PostgreSQL
- Docker
- Uvicorn
- REST
- JSON
- Node-RED
- Pytest
- JavaScript
- Linux / Ubuntu
- WSL2

## To run the project:  

### 1. Clone the repository

```bash
git clone https://github.com/luke-dunlop/robotic-arm-monitor.git
cd robotic-arm-monitor
```
### 2. Create venv

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
python -m pip install -r requirements.txt
```
### 4. Set up environment variables

Copy the example file and fill in real values:
```bash
cp .env.example .env
```
`.env` needs:
```
DATABASE_URL=postgresql+psycopg://robot_user:robot_password@localhost:5432/robot_monitor
API_KEY= choose your own
```
### 5. Start Postgres
```bash
docker compose up -d postgres
```

### 6. Start the FastAPI server
```bash
uvicorn app.main:app
```

The API will be available at: http://127.0.0.1:8000

The documentation available at: http://127.0.0.1:8000/docs

### 7. Run the simulator (in a separate terminal)

```bash
python -m app.simulator
```

### 8. Run the Node-Red dashboard (also separate terminal)

```bash
export API_KEY= same as your env file
node-red
```

Then in the Node-RED editor (http://127.0.0.1:1880), import `robot-monitor.json` from this repo and deploy

### 9. Run the tests

```bash
pytest -v
```


## Future implementations

- MQTT
- Support for multiple robots
- More advanced telemetry simulation
- Experiment with REACT frontend

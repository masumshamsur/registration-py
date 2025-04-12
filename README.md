# Registration Application

This project is a microservice-based application for user registration and authentication. It consists of the following components:

- **Backend**: A FastAPI-based backend for handling API requests and database operations.
- **Frontend**: A Flask-based frontend for user interaction.
- **PostgreSQL**: A database for storing user data.

## Project Structure

```
registration-py/
├── .github/
│   └── workflows/
│       └── ci-cd-pipeline.yaml  # GitHub Actions workflow for CI/CD
├── backend/
│   ├── Dockerfile               # Dockerfile for backend containerization
│   ├── requirements.txt         # Python dependencies for the backend
│   ├── config/
│   │   └── .env                 # Environment variables for the backend
│   ├── src/
│   │   ├── app.py               # Main application entry point
│   │   ├── database.py          # Database connection and setup
│   │   ├── models.py            # Database models
│   │   ├── routes.py            # API routes
│   │   └── schemas.py           # Data validation schemas
│   ├── tests/
│   │   └── test_database.py     # Unit tests for database functionality
├── frontend/
│   ├── Dockerfile               # Dockerfile for frontend containerization
│   ├── requirements.txt         # Python dependencies for the frontend
│   ├── src/
│   │   ├── app.py               # Main application entry point
│   │   ├── static/
│   │   │   └── style.css        # CSS for frontend styling
│   │   └── templates/
│   │       ├── index.html       # HTML template for the main page
│   │       ├── result.html      # HTML template for results
│   │       └── users.html       # HTML template for user list
│   ├── tests/
│   │   └── test_app.py          # Unit tests for frontend functionality
├── k8s/
│   ├── backend-deployment.yaml  # Kubernetes deployment for the backend
│   ├── frontend-deployment.yaml # Kubernetes deployment for the frontend
│   ├── postgres-secret.yaml     # Kubernetes secret for PostgreSQL credentials
│   ├── postgres-statefulset.yaml # Kubernetes StatefulSet for PostgreSQL
│   └── pv-pvc.yaml              # PersistentVolume and PersistentVolumeClaim for PostgreSQL
├── registration-py-chart/
│   ├── registration-backend/
│   │   ├── Chart.yaml           # Helm chart metadata for backend
│   │   ├── values.yaml          # Default values for the backend Helm chart
│   │   └── templates/
│   │       ├── deployment.yaml  # Helm template for backend deployment
│   │       ├── secret.yaml      # Helm template for backend secrets
│   │       └── service.yaml     # Helm template for backend service
│   ├── registration-frontend/
│   │   ├── Chart.yaml           # Helm chart metadata for frontend
│   │   ├── values.yaml          # Default values for the frontend Helm chart
│   │   └── templates/
│   │       ├── deployment.yaml  # Helm template for frontend deployment
│   │       └── service.yaml     # Helm template for frontend service
│   └── registration-statefulset/
│       ├── Chart.yaml           # Helm chart metadata for PostgreSQL StatefulSet
│       ├── values.yaml          # Default values for the PostgreSQL Helm chart
│       └── templates/
│           ├── persistentvolume.yaml # Helm template for PersistentVolume
│           ├── persistentvolumeclaim.yaml # Helm template for PersistentVolumeClaim
│           ├── secrets.yaml     # Helm template for PostgreSQL secrets
│           ├── service.yaml     # Helm template for PostgreSQL service
│           └── statefulset.yaml # Helm template for PostgreSQL StatefulSet
├── registration-py-chart-all-togather/
│   ├── Chart.yaml               # Helm chart metadata for combined deployment
│   ├── values.yaml              # Default values for the combined Helm chart
│   └── templates/
│       ├── backend.yaml         # Helm template for backend deployment and service
│       ├── frontend.yaml        # Helm template for frontend deployment and service
│       └── postgres.yaml        # Helm template for PostgreSQL StatefulSet and service
└── README.md                    # Project documentation
```

### Backend
- **Language**: Python (FastAPI)
- **Dependencies**: Listed in `backend/requirements.txt`
- **Dockerfile**: `backend/Dockerfile`

### Frontend
- **Language**: Python (Flask)
- **Dependencies**: Listed in `frontend/requirements.txt`
- **Dockerfile**: `frontend/Dockerfile`

### Kubernetes
- **Manifests**: Located in the `k8s/` directory
- **Helm Charts**:
  - `registration-py-chart/`: Separate charts for backend, frontend, and PostgreSQL
  - `registration-py-chart-all-togather/`: Combined chart for all components

## CI/CD Pipeline

The CI/CD pipeline is implemented using GitHub Actions. It includes the following steps:
1. **Build and Test**:
   - Runs unit tests for both backend and frontend.
   - Caches Python dependencies to reduce execution time.
2. **Docker Build and Push**:
   - Builds Docker images for backend and frontend.
   - Pushes the images to DockerHub.
3. **Deployment**:
   - Deploys the application to a Kubernetes cluster using Helm.

## Prerequisites

- **Docker**: For building and running containers.
- **Kubernetes**: For deploying the application.
- **Helm**: For managing Kubernetes deployments.
- **GitHub Secrets**:
  - `DOCKERHUB_USERNAME`: DockerHub username.
  - `DOCKERHUB_TOKEN`: DockerHub access token.

## How to Run

### 1. Local Development
- **Backend**:
  ```bash
  cd backend
  pip install -r requirements.txt
  uvicorn src.app:app --reload
  ```

- **Frontend**:
  ```bash
  cd frontend
  pip install -r requirements.txt
  flask run
  ```

### 2. Docker
- **Build and Run Backend**:
  ```bash
  docker build -t registration-backend ./backend
  docker run -p 8000:8000 registration-backend
  ```

- **Build and Run Frontend**:
  ```bash
  docker build -t registration-frontend ./frontend
  docker run -p 5000:5000 registration-frontend
  ```

### 3. Kubernetes
- **Apply Manifests**:
  ```bash
  kubectl apply -f k8s/
  ```

- **Deploy with Helm**:
  ```bash
  helm upgrade --install registration-py-chart ./registration-py-chart-all-togather --namespace registration-fb
  ```

## Testing

- **Run Backend Tests**:
  ```bash
  pytest backend/tests/
  ```

- **Run Frontend Tests**:
  ```bash
  pytest frontend/tests/
  ```

## License

This project is licensed under the MIT License.
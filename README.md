# M87 Gravitational Lensing Visualization

This project creates a unique visualization of Earth and the Solar System as seen through the gravitational lensing effect of the M87 black hole. It combines:

- Gravitational lensing data from M87
- Astronomical data of Earth and the Solar System
- Machine learning for data enhancement
- Stable Diffusion for image generation
- Spectrographic data processing

## Setup

1. Install Python 3.8 or higher
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

- `data_fetcher.py`: Fetches astronomical data from various sources
- `lensing_processor.py`: Processes gravitational lensing effects
- `ml_enhancer.py`: Machine learning models for data enhancement
- `image_generator.py`: Generates final visualizations using Stable Diffusion
- `main.py`: Main script to run the entire pipeline

## Usage

Run the main script:
```bash
python main.py
```

## Data Sources

- M87 gravitational lensing data from Event Horizon Telescope
- Solar System data from NASA's JPL HORIZONS system
- Spectrographic data from various astronomical databases

## OpenShift Deployment

The project can be deployed to OpenShift for daily automated visualizations.

### Prerequisites

1. OpenShift CLI (`oc`) installed
2. Docker installed
3. Access to a container registry
4. OpenShift cluster access

### Deployment Steps

1. Set your container registry:
   ```bash
   export DOCKER_REGISTRY="your-registry.example.com"
   ```

2. Make the deployment script executable:
   ```bash
   chmod +x deploy.sh
   ```

3. Run the deployment script:
   ```bash
   ./deploy.sh
   ```

### Deployment Configuration

The deployment includes:
- A persistent volume for storing visualizations
- A daily CronJob that runs at midnight
- Resource limits and requests for optimal performance
- Automatic image building and pushing

### Accessing Results

The visualizations are stored in a persistent volume and can be accessed through:
1. OpenShift console
2. Direct pod access
3. Volume mount in other pods

### Monitoring

You can monitor the daily runs through:
```bash
oc get cronjobs
oc get pods
oc logs -f <pod-name>
```

### Customization

To modify the schedule or resources:
1. Edit `openshift-deployment.yaml`
2. Re-run the deployment script

The default configuration:
- Runs daily at midnight
- Uses 2GB memory and 1 CPU core
- Stores visualizations in a 10GB persistent volume 

**Credits:**
This project benefited from AI code assistance by [Cursor](https://www.cursor.com/). 
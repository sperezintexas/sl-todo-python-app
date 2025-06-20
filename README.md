# FastAPI Todo API Demo with Sealights

This demo project showcases a simple Todo API built with FastAPI, demonstrating test instrumentation and deployment practices. The project includes Docker containerization, GitHub Actions CI/CD, and deployment to Google Kubernetes Engine (GKE).

## Project Structure

## Features

- RESTful Todo API with CRUD operations
- FastAPI for high performance and automatic OpenAPI documentation
- Pytest for testing
- Multi-stage Docker builds
- GitHub Actions CI/CD pipeline
- GKE deployment with Kubernetes
- Artifact Registry integration

## Prerequisites

- Python 3.11+
- Docker
- Google Cloud Platform account
- kubectl
- A GCP project with required APIs enabled:
  - Container Registry API
  - Kubernetes Engine API
  - Artifact Registry API

## Local Development

1. Create and activate virtual environment:
2. Install dependencies:
3. Run the application:

## Troubleshooting

Common issues and solutions:
1. Image pull errors:
   - Verify Artifact Registry permissions
   - Check image path and tags

2. Pod startup failures:
   - Check logs: `kubectl logs <pod-name>`
   - Verify resource limits

3. Deployment fails:
   - Check GitHub Actions logs
   - Verify GCP service account permissions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License. See LICENSE file for details.
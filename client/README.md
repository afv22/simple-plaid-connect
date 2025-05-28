## Running the Project with Docker

This project is containerized using Docker and Docker Compose for easy setup and deployment. Below are the instructions and details specific to this project:

### Requirements
- **Node.js version:** The Dockerfile uses `node:22.13.1-slim`. No need to install Node.js locally; Docker handles it.
- **No external services** (e.g., databases) are required.

### Environment Variables
- No required environment variables are set by default. If you need to add any, uncomment and use the `env_file` section in `docker-compose.yml`.

### Build and Run Instructions
1. **Build and start the app:**
   ```sh
   docker compose up --build
   ```
   This will build the Docker image and start the application container.

2. **Access the app:**
   - The app will be available at [http://localhost:8080](http://localhost:8080)

### Ports
- **8080:** Exposed by the container and mapped to your host. This is where the Vite preview server runs.

### Special Configuration
- The app runs as a non-root user (`appuser`) inside the container for improved security.
- The build process uses multi-stage builds to optimize the final image size and only includes production dependencies.
- If you want to enable live code reload for development, uncomment and configure the `volumes` section in `docker-compose.yml`.

---

*These instructions are specific to this project's Docker setup. For further customization, refer to the `Dockerfile` and `docker-compose.yml`.*

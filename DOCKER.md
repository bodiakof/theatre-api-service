### Prerequisites

  - [Docker](https://docs.docker.com/get-docker/)
  - [Docker Compose](https://docs.docker.com/compose/install/)

### Setup Instructions

1. **Clone the Repository:**
  
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```
<br>

2. **Create the Environment File:**
  
   A sample environment file is provided as `.env.sample`. Copy it to create your own `.env` file and update the variables as needed:
  
   ```bash
   cp .env.sample .env
   ```
<br>

3. **Build and Run the Containers:**
  
   Use Docker Compose to build the images and start the containers:
  
   ```bash
   docker-compose up --build
   ```
  
   This command will:
   - Build the Docker image using the provided `Dockerfile`.
   - Start the Django application (`app` service) and the PostgreSQL database (`db` service).
   - Map port 8000 so you can access the API at [http://localhost:8000](http://localhost:8000).
   
   <br>

4. **Apply Database Migrations:**
  
   The `docker-compose` command automatically runs migrations. If you need to run migrations manually, execute:
  
   ```bash
   docker-compose exec app python manage.py migrate
   ```
<br>

5. **Load Fixture Data:**
  
   To populate the database with initial data from `fixtures.json`, run:
  
   ```bash
   docker-compose exec app python manage.py loaddata fixtures.json
   ```
<br>

6. **Access the Application:**
  
   Once everything is up and running, open your browser and navigate to [http://localhost:8000](http://localhost:8000) to access the API.

### Docker File Overview

  - **Dockerfile:**
    - Uses the Python 3.10 Alpine image.
    - Installs dependencies from `requirements.txt`.
    - Sets `PYTHONUNBUFFERED=1` for real-time logging.
    - Creates a non-root user (`django-user`) and adjusts file permissions.
    - Copies the project files into the container and sets the working directory.
    - Runs as the non-root user.


  - **docker-compose.yaml:**
    - **app:**  
      Builds and runs the Django application.
      - Uses the `wait_for_db` script to ensure the database is ready.
      - Runs migrations automatically and starts the development server on `0.0.0.0:8000`.
      - Mounts the project directory and media volume.
    - **db:**  
      Runs a PostgreSQL container using the `postgres:16.0-alpine3.17` image with persistent storage.

<br>

With these instructions, you should be able to easily set up and run the project using Docker. Happy coding!
# API Endpoints Documentation

  This document provides a detailed list of all available API endpoints for the Theatre API Service, including sample request bodies and descriptions.

  ---

  ## User Endpoints

  ### Registration & Authentication

  - **POST** `/api/users/register/`  
    **Description:** Register a new user.  
    **Sample Request Body:**
    ```json
    {
      "email": "user@example.com",
      "password": "securepassword123"
    }
    ```
<br>

  - **POST** `/api/users/token/obtain/`  
    **Description:** Obtain a JWT token for authentication.  
    **Sample Request Body:**
    ```json
    {
      "email": "user@example.com",
      "password": "securepassword123"
    }
    ```
<br>

  - **POST** `/api/users/token/refresh/`  
    **Description:** Refresh the JWT access token.  
    **Sample Request Body:**
    ```json
    {
      "refresh": "your_jwt_refresh_token"
    }
    ```
<br>

  - **POST** `/api/users/token/verify/`  
    **Description:** Verify if a JWT token is valid.  
    **Sample Request Body:**
    ```json
    {
      "token": "your_jwt_access_token"
    }
    ```

  ### User Profile

  - **GET** `/api/users/me/`  
    **Description:** Retrieve details of the authenticated user.  
    **Headers:**
    ```
    Authorization: Bearer <your_jwt_access_token>
    ```
<br>

  - **PATCH** `/api/users/me/`  
    **Description:** Update details of the authenticated user.  
    **Headers:**
    ```
    Authorization: Bearer <your_jwt_access_token>
    ```  
    **Sample Request Body (e.g., updating email):**
    ```json
    {
      "email": "new_email@example.com"
    }
    ```

  ---

  ## Theatre Endpoints

  ### Genres

  - **GET** `/api/theatre/genres/`  
    **Description:** List all genres.

  - **POST** `/api/theatre/genres/`  
    **Description:** Create a new genre.  
    **Sample Request Body:**
    ```json
    {
      "name": "Comedy"
    }
    ```

  ---

  ### Actors

  - **GET** `/api/theatre/actors/`  
    **Description:** List all actors.

  - **POST** `/api/theatre/actors/`  
    **Description:** Create a new actor.  
    **Sample Request Body:**
    ```json
    {
      "first_name": "Emma",
      "last_name": "Stone"
    }
    ```

  ---

  ### Theatre Halls

  - **GET** `/api/theatre/theatre-halls/`  
    **Description:** List all theatre halls.

  - **POST** `/api/theatre/theatre-halls/`  
    **Description:** Create a new theatre hall.  
    **Sample Request Body:**
    ```json
    {
      "name": "Main Hall",
      "rows": 20,
      "seats_in_row": 30
    }
    ```

  ---

  ### Plays

  - **GET** `/api/theatre/plays/`  
    **Description:** List plays with filtering options.  
    **Query Parameters:**  
      - `title`: Filter by play title (e.g., `?title=hamlet`)  
      - `genres`: Comma-separated genre IDs (e.g., `?genres=2,5`)  
      - `actors`: Comma-separated actor IDs (e.g., `?actors=1,3`)

  - **POST** `/api/theatre/plays/`  
    **Description:** Create a new play.  
    **Sample Request Body:**
    ```json
    {
      "title": "Hamlet",
      "description": "A Shakespearean tragedy.",
      "genres": [1, 2],
      "actors": [1, 3]
    }
    ```
<br>

  - **GET** `/api/theatre/plays/{id}/`  
    **Description:** Retrieve details of a specific play.

  - **POST** `/api/theatre/plays/{id}/upload-image/`  
    **Description:** Upload an image for a play (admin-only).  
    **Headers:**
    ```
    Authorization: Bearer <your_admin_jwt_access_token>
    ```  
    **Note:** Use `multipart/form-data` for the image file.

  ---

  ### Performances

  - **GET** `/api/theatre/performances/`  
    **Description:** List performances with filtering options.  
    **Query Parameters:**  
      - `play`: Filter by play ID (e.g., `?play=3`)  
      - `date`: Filter by date (format: YYYY-MM-DD, e.g., `?date=2025-01-01`)

  - **POST** `/api/theatre/performances/`  
    **Description:** Create a new performance.  
    **Sample Request Body:**
    ```json
    {
      "play": 1,
      "theatre_hall": 1,
      "show_time": "2025-03-10T19:30:00Z"
    }
    ```
<br>

  - **GET** `/api/theatre/performances/{id}/`  
    **Description:** Retrieve details of a specific performance.

  - **PUT/PATCH/DELETE** `/api/theatre/performances/{id}/`  
    **Description:** Update or delete a performance.

  ---

  ### Reservations

  - **GET** `/api/theatre/reservations/`  
    **Description:** List reservations for the authenticated user.  
    **Headers:**
    ```
    Authorization: Bearer <your_jwt_access_token>
    ```
<br>

  - **POST** `/api/theatre/reservations/`  
    **Description:** Create a new reservation.  
    **Headers:**
    ```
    Authorization: Bearer <your_jwt_access_token>
    ```  
    **Sample Request Body:**
    ```json
    {
      "performance": 1,
      "seats": ["A1", "A2", "A3"]
    }
    ```

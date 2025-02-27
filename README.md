# Theatre API Service

The Theatre API Service is a Django-based backend designed for managing a theatre booking system. It provides endpoints for user management, theatre data (genres, actors, theatre halls, plays, performances), and reservations, along with JWT-based authentication.

## Features

- **User Management**  
  - **Registration:** Create a new user account.
  - **Profile:** Retrieve and update the authenticated user's profile.
  - **Authentication:** JWT endpoints for obtaining, refreshing, and verifying tokens.



- **Theatre Management**  
  - **Genres:** Create and list genres.
  - **Actors:** Create and list actors.
  - **Theatre Halls:** Manage theatre halls with seating information.
  - **Plays:**  
    - Create, list, and retrieve plays.
    - Filter plays by title, genre IDs, and actor IDs.
    - Upload images for plays (admin-only feature).
  - **Performances:**  
    - Create, list, retrieve, update, and delete performances.
    - Filter performances by play and date.
    - Automatically calculate available tickets based on theatre hall capacity.
  - **Reservations:**  
    - Create and list reservations for the authenticated user.
    - Reservations are automatically scoped to the current user.



- **Pagination**  
  Custom pagination is implemented via `PlayAndReservationPaginator` to control the number of items per page and simplify client-side data handling.

## Business Logic

- **Plays Filtering:**  
  Filter plays by providing query parameters such as `title` (partial match), `genres` (comma-separated IDs), and `actors` (comma-separated IDs).


- **Ticket Availability Calculation:**  
  For each performance, available tickets are computed as ```(theatre_hall.rows * theatre_hall.seats_in_row) - number_of_tickets_sold```


- **Image Upload:**  
Admin users can upload images for plays via the `upload-image` action on the play endpoint.


- **User Reservations:**  
Reservations are strictly tied to the authenticated user, ensuring privacy and data consistency.
  
## API Endpoints

You can find a detailed list of all API endpoints [here](API_ENDPOINTS.md).


## Running the Project with Docker

This project is containerized with Docker to simplify setup and ensure consistency across environments. Follow [these steps](DOCKER.md) to run the project on your local machine.



# Clan Map Generator

A Flask web application that generates an interactive map visualization of clan members' locations using Folium and OpenStreetMap data.

## Features

- Interactive world map showing clan member locations
- Geocoding integration with OpenStreetMap Nominatim API
- Responsive web interface
- Docker containerization for easy deployment
- Flask-based web server

## Project Structure

```
clan-map/
├── app.py              # Main Flask application
├── map_generator.py    # Map generation logic
├── clan_data.json      # Clan member data
├── requirements.txt    # Python dependencies
├── Dockerfile         # Docker configuration
├── templates/
│   └── map.html       # Generated map template
└── README.md          # This file
```

## Installation & Setup

### Local Development

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd clan-map
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Access the application:**
   Open your browser and navigate to `http://localhost:5010`

### Docker Deployment

1. **Build the Docker image:**
   ```bash
   docker build -t clan-map .
   ```

2. **Run the container:**
   ```bash
   docker run -p 5000:5000 clan-map
   ```

3. **Access the application:**
   Open your browser and navigate to `http://localhost:5000`

## Configuration

### Clan Data

Edit `clan_data.json` to add or modify clan member information:

```json
[
  {
    "name": "Member Name",
    "location": "City, Country"
  }
]
```

**Note:** Use "Unknown" for location if the member's location is not available.

### Port Configuration

- **Development:** The app runs on port 5010 (configurable in `app.py`)
- **Production (Docker):** The app runs on port 5000 via Gunicorn

## API Integration

The application uses the OpenStreetMap Nominatim API for geocoding locations. No API key is required, but please be respectful of rate limits.

## Dependencies

- **Flask:** Web framework
- **Folium:** Interactive map generation
- **Requests:** HTTP client for geocoding API
- **Gunicorn:** Production WSGI server (Docker only)

## Development

### Adding New Features

1. Modify `map_generator.py` for map-related functionality
2. Update `app.py` for new routes or Flask configurations
3. Edit `clan_data.json` to update member information

### Testing

The application can be tested locally using the Flask development server:

```bash
python app.py
```

## Production Considerations

- The Docker container uses Gunicorn with 2 workers
- The application runs as a non-root user for security
- Consider implementing caching for geocoding results in high-traffic scenarios
- Rate limiting may be needed for the geocoding API

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

[Add your license information here]

## Support

[Add contact information or support channels here]

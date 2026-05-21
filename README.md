# Edu-Metric CRM

Edu-Metric CRM platform.

## 🚀 Running the Project

1. Build and run the services with Docker Compose:
   ```bash
   docker compose up -d --build
   ```

2. The services are exposed on the following ports:
   - **Frontend**: `http://localhost:3005`
   - **Gateway (API Gateway)**: `http://localhost:8080`
   - **Backend (Django API)**: `http://localhost:8000`
   - **Database (PostgreSQL)**: `http://localhost:5432`
   - **Redis**: `http://localhost:6379`

---

## 🌐 Host Nginx Setup

Since Nginx runs natively on the host server on port 80, we route incoming traffic to the Docker containers via a reverse proxy configuration on the host.

### 1. Copy Configuration
Copy the host configuration file located at `nginx/host_nginx.conf` to your host's Nginx configuration directory (e.g., `/etc/nginx/sites-available/`):

```bash
sudo cp nginx/host_nginx.conf /etc/nginx/sites-available/shahzod.conf
```

### 2. Enable Site
Enable the site by linking it to the `sites-enabled` directory:

```bash
sudo ln -s /etc/nginx/sites-available/shahzod.conf /etc/nginx/sites-enabled/
```

### 3. Test & Reload Nginx
Verify the configuration is correct and reload Nginx:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

### 4. Optional: Setup Let's Encrypt SSL
If you want to configure HTTPS, use Certbot to automatically configure SSL certificates:

```bash
sudo certbot --nginx -d shahzod.app -d www.shahzod.app -d api.shahzod.app
```
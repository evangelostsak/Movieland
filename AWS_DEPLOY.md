# Deploying Movieland on an Existing EC2 Instance

This guide will help you deploy **Movieland** on an existing EC2 instance running **Amazon Linux**.  
The app requires **Python 3, PostgreSQL, Docker, and Git**.  

---

## Prerequisites  

- Ensure your **EC2 instance** is set up and running.  
- You have the **.pem key** to access your EC2 instance.  
- You know the **public IP** of your EC2 instance.  
- **Security Group**: Ensure ports **5000 (Flask)** and **5432 (PostgreSQL, if remote)** are open.  

---

## Step 1: Connect to Your EC2 Instance  

Open your terminal and use SSH to connect:  

```bash
ssh -i /path/to/your-key.pem ec2-user@your-ec2-public-ip
```

---

## Step 2: Update Your EC2 Instance  

```bash
sudo yum update -y
```

---

## Step 3: Install Git  

```bash
sudo yum install git -y
```

Verify:  

```bash
git --version
```

---

## Step 4: Install Python3 and Pip  

```bash
sudo yum install python3 python3-pip -y
```

Verify:  

```bash
python3 --version
pip3 --version
```

---

## Step 5: Install Docker & Docker Compose  

Movieland will run inside **Docker** for easier deployment.  

```bash
sudo yum install docker -y
```

Start Docker and enable it to run on boot:  

```bash
sudo systemctl start docker
sudo systemctl enable docker
```

Verify Docker installation:  

```bash
docker --version
```

Install **Docker Compose**:  

```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

Verify:  

```bash
docker-compose --version
```

---

## Step 6: Install PostgreSQL (if using local DB)  

> **Note**: If you're using **Amazon RDS** for PostgreSQL, skip this step.  

Install PostgreSQL 15:  

```bash
sudo dnf install postgresql15 postgresql15-server postgresql15-contrib -y
```

Initialize the database:  

```bash
sudo /usr/pgsql-15/bin/postgresql-15-setup initdb
```

Start and enable PostgreSQL:  

```bash
sudo systemctl start postgresql-15
sudo systemctl enable postgresql-15
```

Switch to the PostgreSQL user:  

```bash
sudo -u postgres psql
```

Create a database and user for **Movieland**:  

```sql
CREATE DATABASE movieland;
CREATE USER movieland_user WITH ENCRYPTED PASSWORD 'securepassword';
GRANT ALL PRIVILEGES ON DATABASE movieland TO movieland_user;
\q
```

---

## Step 7: Clone Movieland Repository  

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/movieland.git
cd movieland
```

---

## Step 8: Configure Environment Variables  

Create a **.env** file in the project root:  

```bash
touch .env
nano .env
```

Add the following variables:  

```ini
FLASK_APP=app.py
FLASK_ENV=production
DATABASE_URL=postgresql://movieland_user:securepassword@db/movieland
SECRET_KEY=your-secret-key
```

Save and exit (`CTRL+X`, then `Y`, then `ENTER`).

---

## Step 9: Set Up Docker  

Create a `Dockerfile` in the root directory:  

```Dockerfile
# Use Python base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask runs on
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
```

Create a `docker-compose.yml` file:  

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    restart: always
    environment:
      POSTGRES_DB: movieland
      POSTGRES_USER: movieland_user
      POSTGRES_PASSWORD: securepassword
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  app:
    build: .
    restart: always
    depends_on:
      - db
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://movieland_user:securepassword@db/movieland
      - FLASK_APP=app.py
      - FLASK_ENV=production
      - SECRET_KEY=your-secret-key

volumes:
  postgres_data:
```

---

## Step 10: Run the Application with Docker  

Start the application:  

```bash
docker-compose up -d
```

Check running containers:  

```bash
docker ps
```

To see logs:  

```bash
docker logs movieland_app
```

---

## Step 11: Configure Security Groups for Flask (Port 5000)  

1. Go to **AWS Console** > **EC2** > **Security Groups**.  
2. Select your instance’s security group.  
3. Edit **Inbound Rules**:  
   - **Protocol**: TCP  
   - **Port**: 5000  
   - **Source**: Your IP (or **0.0.0.0/0** for public access)  
4. Save changes.  

---

## Step 12: Automate App Restart with Systemd  

Create a **Systemd service**:  

```bash
sudo nano /etc/systemd/system/movieland.service
```

Add the following:  

```ini
[Unit]
Description=Movieland Flask App
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/movieland
ExecStart=/usr/bin/docker-compose up
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:  

```bash
sudo systemctl daemon-reload
sudo systemctl enable movieland
sudo systemctl start movieland
```

Check logs:  

```bash
sudo journalctl -u movieland --follow
```

---

## Step 13: Verify Deployment  

Your Movieland app should now be running at:  

```bash
http://your-ec2-public-ip:5000
```

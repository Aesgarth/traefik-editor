# **Traefik Config Editor**  

A simple web-based editor for managing Traefik’s **`dynamic.yml`** file.  
This tool provides a **basic UI** for editing HTTP routers, services, and middlewares directly in your browser.  

🚀 **Features**:
- Edit `dynamic.yml` with **YAML syntax highlighting**  
- Manage routers, services, and middlewares via tables & forms  
- **Dark mode support** for improved readability  
- **Automatic backups** of configuration changes  
- **Dockerized** for easy deployment  

🚠 **Note:** This is a **basic configuration editor**. It does not include **validation or advanced error handling**. Use with caution.

---

## **🚀 Installation & Setup**  
The recommended way to deploy this tool is **via Docker Compose**.

### **1️⃣ Find Your Traefik `dynamic.yml` File**  
Make sure you know where **Traefik’s `dynamic.yml`** file is located. Common paths:
```sh
/opt/traefik/config/dynamic.yml
/etc/traefik/dynamic.yml
/path/to/traefik/data/configs/dynamic.yml
```

---

### **2️⃣ Find the Docker User ID (UID)**
To ensure the container has **write access** to the `dynamic.yml` file, check the **UID** of the user running inside Docker:

```sh
docker run --rm aesgarth/traefikeditor:latest id
```
💪 Example output:
```
uid=5678(appuser) gid=5678(appuser) groups=5678(appuser),100(users)
```
Here, **5678** is the UID.

Now, **grant write permissions to this UID**:
```sh
setfacl -m u:5678:rw /path/to/traefik/dynamic.yml
```
💪 Now, the container will be able to edit the file.

---

### **3️⃣ Deploy Using Docker Compose**
Create a `docker-compose.yml` file:
```yaml
version: '3.4'

services:
  traefikeditor:
    image: aesgarth/traefikeditor:latest
    build:
      context: .
      dockerfile: ./Dockerfile
    ports:
      - 8000:8000
    volumes:
      - /path/to/traefik/data/configs/dynamic.yml:/data/dynamic.yml  # Mount your YAML file
```

💪 **Run the container**:
```sh
docker-compose up -d
```
**The editor will now be available at:**  
📌 `http://your-server-ip:8000`

---

## **🔄 Updating the Container**
To pull the latest version and restart:
```sh
docker-compose pull
docker-compose up -d
```
💪 This ensures you always run the latest release.

---

## **⚠ Security Considerations**
- **DO NOT expose this editor publicly** without securing it behind authentication.  
- **Use Traefik access controls** to restrict access.  
- **Back up your `dynamic.yml`** before making significant changes.  

---

## **💡 Troubleshooting**
### **YAML Won’t Save?**
Ensure the container has **write access**:
```sh
getfacl /path/to/traefik/dynamic.yml
```
If needed, **grant permissions**:
```sh
setfacl -m u:5678:rw /path/to/traefik/dynamic.yml
```
_(Replace `5678` with your actual Docker user ID.)_

---

## **🛠 Contributing**
This is a basic tool, and improvements are welcome!  
Feel free to **submit pull requests** or report issues on GitHub.

---

## **🐝 License**
This project is released under the **MIT License**.

---

### **💪 Now, You’re Ready to Manage Traefik Configuration Easily!**
Let me know if you'd like any modifications! 🚀🔥


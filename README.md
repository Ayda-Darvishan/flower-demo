# Flower Studio — educational Streamlit demo
Includes 10 supplied product photos, Persian catalogue, search, cart and simulated summary. Product names and USD prices are placeholders. No payment, real order submission, personal-data collection or persistent database.

## Local run (Python 3.10+)
From this folder:
```bash
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows PowerShell instead:
# .venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```
Open http://localhost:8501. Edit products.json to change names, descriptions and sample prices. Keep the images folder alongside app.py.

## Educational hosting
Only publish with permission to use the photos and after checking provider terms and eligibility. Hosting is not authorization for a commercial Iran-related activity.

Streamlit Community Cloud: upload app.py, requirements.txt, products.json and images to a GitHub repository, connect the repository in Community Cloud and select app.py as entrypoint. No Docker needed for that route.

AWS EC2 / Google Compute Engine: use an eligible Linux VM with Docker installed, copy this folder, then:
```bash
docker build -t flower-demo .
docker run -d --restart unless-stopped -p 127.0.0.1:8501:8501 --name flower-demo flower-demo
```
This binds only to localhost. For public hosting put a HTTPS reverse proxy (Nginx or Caddy) in front of localhost:8501 with WebSocket support. Point domain DNS to the VM, allow inbound 80/443, restrict SSH to your own IP, and keep 8501 private. Configure OS updates and cost alerts. These commands are not a complete production deployment.

Cloud Run needs a container listening on the configured port (8501 for this image), WebSocket timeout/reconnection planning and appropriate session handling. Local/session state is temporary.

Before real commerce: licensed/accepted payment provider, verified server-side payment confirmation, persistent database, inventory and fulfillment process, privacy/access controls, backups and monitoring. Do not collect payment-card data in Streamlit.

# CareerPilot

### Set up Secrets

Create a `secrets.toml` file inside a `.streamlit` folder at the project root directory and add your Replicate API token inside of it. Inside `.streamlit/secrets.toml`:

```
REPLICATE_API_TOKEN="your_token_here"
```

### Run application locally without Docker

1. Install Python 3.9 or newer from [Python's official website](https://www.python.org/downloads/).
2. Create a Python virtual environment with `python -m venv .venv` (`python -m venv venv` on Windows).
3. Run `. .venv/bin/activate` (`venv\Scripts\activate` on Windows).
4. Install the required Python dependencies using:
   ```bash
   pip install -r requirements.txt
   ```
5. To start the app, run the following command from the project root:
   ```bash
   streamlit run Home.py --server.port=8501 --server.address=0.0.0.0
   ```

### Build and run application in Docker

Install Docker from [Docker's official website](https://www.docker.com/products/docker-desktop).

To start the app, run the following command from the project root:

```bash
docker build -t app . && docker run -p 8501:8501 app
```

### Access the application

Visit http://localhost:8501 in your browser to interact with the Streamlit application.

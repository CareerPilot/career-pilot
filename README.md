#### Prerequisites

Install Docker from [Docker's official website](https://www.docker.com/products/docker-desktop).

#### Set Up Secrets

Create a `secrets.toml` file inside the `.streamlit` folder at the root of your project directory and add your Replicate API token inside of it:

```
REPLICATE_API_TOKEN="your_token_here"
```

#### Build and Run the Docker Container

Execute the following command in the terminal within the project directory:

```bash
docker build --no-cache -t my-streamlit-app . && docker run -p 8501:8501 my-streamlit-app
```

### Access the Application

Visit http://localhost:8501 in your browser to interact with the Streamlit application.

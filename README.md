# CareerPilot

## Configuration and Installation

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

## Architecture

This application consists of two components, the Web front-end, using Streamlit, and the Llama-3 LLM.  Streamlit is a rapid
development Web framework in Python.  It allowed us to quickly construct the Website to serve the necessary content, collect the
data from the user to give to the LLM, and display the results of the LLM with an additional chat interface.

All code is in Python.  There are supporting packages to parse PDF and DOCX files as a convenience for the user.  We used the
Replicate package to access the LLM since it provides a convenient interface without requiring manual deployment of the LLM.  We
were unable to deploy the IK-specified Llama-2 LLM due to configuration problems.  However, we believe using the Replicate service
provides a better experience since it has access to the Llama-3 LLM.

## Deployment

This application is in a Docker container and deployed to AWS using Amazon Elastic Container Service
[ECS](https://aws.amazon.com/ecs/).  All configuration was done in the AWS console, including the credentials required to access
the Replicate service.

## Usage

After deploying the application, visit its URL to see the first page that accepts the resume and job description.  The resume can
be either text pasted into a text box or a file uploaded by browsing the user's file system.  After submitting, these required
parameters, the Website invokes the LLM.  After a short time, it responds with the results of the LLM.  The user may review this
at their leisure.  If they so desire, they may start a chat session with the LLM to further improve the results.

## Fine-tuning

Fine-tuning the Large Language Model used in this application can be achieved with the following steps.

1. Start with the Llama-3 LLM.
1. Collect training data that is relevant to the specific task, in this case, job-related data such as resumes and evaluations.
1. Tokenize the data, which are small units of text the model can understand.
1. Train using the tokenized data.

The last step involves adapting the pre-trained model to specific tasks by updating parameters on a new dataset.  There are two
ways to customize the model with fine-tuning, either supervised learning or reinforcement learning from human feedback (RLHF).
Both have their advantages and disadvantages, such as differing amounts of human effort required versus quality of training.

## Screenshots

<figure>
	<img src="images/Screen 1.png">
	<figcaption>This is the initial view of the application</figcaption>
</figure>

<figure>
	<img src="images/Screen 2.png">
	<figcaption>This is the view of the application after uploading a document and providing the job description</figcaption>
</figure>

<figure>
	<img src="images/Screen 3.png">
	<figcaption>This is the view of the application waiting for the result after clicking "View Coaching Report"</figcaption>
</figure>

<figure>
	<img src="images/Screen 4.png">
	<figcaption>This is the view of the application after the LLM provides its response</figcaption>
</figure>

<figure>
	<img src="images/Screen 5.png">
	<figcaption>This is the view of the Resume Coach section of the application with a question</figcaption>
</figure>

<figure>
	<img src="images/Screen 6.png">
	<figcaption>This is the view of the Resume Coach section of the application with a response to the question</figcaption>
</figure>

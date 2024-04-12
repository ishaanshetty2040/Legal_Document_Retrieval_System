
# Legal Sarathi

Legal Sarathi Our idea tackles a significant issue that attorneys in Indian courts deal with: the laborious and prone to error manual analysis of unstructured legal case documents.Insufficient contextual knowledge frequently causes delays and imprecise case comprehension. We suggest creating an automated event extraction tool as a solution to this. This program efficiently extracts important events, important players and timelines. Optimizing case analysis through an intuitive interface, guaranteeing prompt and precise insights.


![Logo](https://raw.githubusercontent.com/ishaanshetty2040/Legal_Document_Retrieval_System/main/LOGO-PROJECT.png)


## Installation

To get started with Legal Sarathi, follow these simple steps:

### Prerequisites
Docker installed on your system

### Step 1: Clone the Repository

```bash
git clone https://github.com/ishaanshetty2040/Legal_Document_Retrieval_System.git

cd Legal case Retrieval
```
### Step 2: Build the Docker Image
We have provided a Dockerfile to streamline the setup process. Execute the following command to build the Docker image:
```bash
docker build -t myLegalSarathi .

```

### Step 3: Verify the Image Creation:
To ensure your image has been created and is listed among your local Docker images, run:
```bash
docker images

```
You should see **myLegalSarathi** in the list of available images

### Step 4: Run the Container
Once the Docker image is built successfully, run the container using the following command:
```bash
docker run -d --name project-container myLegalSarathi


```
Congratulations! You have successfully set up Legal Sarathi on your system.


## Acknowledgements




## Demo

https://vimeo.com/933791552


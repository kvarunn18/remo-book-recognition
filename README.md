# remo-book-recognition

The goal of this project is to develop a system that can scan book covers and extract relevant metadata for database entry. The system should capture both front and back covers and extract key bibliographic information including title, creators, copyright date, summary, series information, genres, form, format, ISBN, page count, and book type.

Team Members:  
- Karthik Varunn Saseendran - saseendran.k@northeastern.edu | karthikvarunn2002@gmail.com | [LinkedIn](https://www.linkedin.com/in/karthikvarunn/)
- Paul Adaimi - adaim.p@northeastern.edu | adaimi.paul@gmail.com | [LinkedIn](https://www.linkedin.com/in/paul-adaimi-aa5b76172/)

## Camera Setup

1. Download and install [**IP Webcam**](https://play.google.com/store/apps/details?id=com.pas.webcam&hl=en) application on your android phone.
2. Make sure your PC and Phone are connected to the same network.
3. Open the IP Webcam application on your phone and click "Start Server" (usually at the bottom).
4. This will open a camera stream on your phone.
5. An IPV4 URL will be displayed on the phone screen.
6. Type the same URL in your PC browser.
7. Scroll down and click "advanced settings".
8. Change the orientation to "portrait".
9. Set the resolution to the highest available option for better results.
10. Note down the URL address, as this will be used to create the `CAMERA_IP` variable (without the port).
11. Make sure to keep the IP Webcam app open before running the `main.py` script.

## Open AI Keys
Here are the steps to get an OpenAI API key:

1. Go to the OpenAI website (https://openai.com/) and sign up for an account if you don't already have one.
2. Once logged in, click on your profile picture in the top right and select "View API keys". 
3. On the API keys page, click the "Create new secret key" button.
4. This will generate a new API key for you. Copy this key and keep it secure, as you'll need to include it in your .env file for your project.
5. You'll also need to get your OpenAI organization ID. You can find this by going to the "API" section in the sidebar, then clicking on "Manage organizations". Copy the organization ID listed there.
6. Finally, you'll need to create an OpenAI project. Go to the "API" section again, then click "Manage projects". Create a new project and copy the project ID.
7. OpenAI offers both paid and free tiers of their language models. Depending on which tier you want to use, you'll need to set the `OPENAI_MODEL_ID` environment variable accordingly in your .env file.
8. Add all of these values (API key, organization ID, project ID, and model ID) to your project's .env file using the variable names specified in the next section.

## Prerequisites

- conda
- pip
- .env file with the following variables:

  ```
  CAMERA_IP="[your_camera_ip_address]"
  OPENAI_API_KEY="[your_openai_api_key]"
  OPENAI_ORG_ID="[your_openai_org_id]"
  OPENAI_PROJECT_ID="[your_openai_project_id]"
  OPENAI_MODEL_ID="[your_openai_preferred_model_id]"
  GOOGLE_BOOKS_API_URL="https://www.googleapis.com/books/v1/volumes"
  ```

## Installation

1. Create a new virtual environment:
   ```
   conda create -n bookreg python=3.8
   ```
2. Activate the virtual environment:
     ```
     conda activate bookreg
     ```
3. Install PyTorch:
     ```
    conda install pytorch torchvision torchaudio cudatoolkit=10.2 -c pytorch
     ```
4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Project

1. Navigate to the project directory:
   ```
   cd /path/to/your/project
   ```
2. Run the main script:
   ```
   python main.py
   ```

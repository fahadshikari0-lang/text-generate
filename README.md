# AI Text & Image Generation Model

An AI-based application that can work with both **text and images**.

This project provides two main capabilities:

* **Text-to-Image:** Generate an image from a text prompt.
* **Image-to-Text:** Analyze an image and generate a text description based on its content.

## Features

### 🖼️ Text-to-Image

Enter a text prompt and the model generates an image according to the provided description.

**Example:**

```text
Prompt:
A futuristic city at night with neon lights
```

The model generates an image based on the prompt.

### 📝 Image-to-Text

Upload an image and the model analyzes it to generate a text description of what is present in the image.

**Example:**

```text
Image:
A dog sitting on the grass

Generated Text:
A dog is sitting on a grassy field.
```

## Project Structure

```text
text-generate/
│
├── app.py
├── model.py
├── frontend.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Technologies Used

* Python
* Hugging Face
* PyTorch
* AI/Deep Learning Models
* Streamlit
* FastAPI

## Installation

Clone the repository:

```bash
git clone https://github.com/fahadshikari0-lang/text-generate.git
```

Go to the project directory:

```bash
cd text-generate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project directory:

```env
HF_TOKEN=your_huggingface_token
```

**Do not upload your `.env` file to GitHub.**

Make sure `.env` is included in `.gitignore`.

## Running the Application

Run the application using the appropriate Python file:

```bash
python app.py
```

For the Streamlit frontend:

```bash
streamlit run frontend.py
```

## How It Works

The application accepts either a **text prompt** or an **image** as input.

### Text → Image

```text
Text Prompt
     ↓
AI Model
     ↓
Generated Image
```

### Image → Text

```text
Image
  ↓
AI Vision Model
  ↓
Generated Text Description
```

## Use Cases

This project can be used for:

* AI image generation
* Image captioning
* Visual content analysis
* Creative content generation
* AI-powered applications
* Text and image experimentation

## Author

**Fahad Shikari**

GitHub:
https://github.com/fahadshikari0-lang

## License

This project is intended for educational and experimental purposes.

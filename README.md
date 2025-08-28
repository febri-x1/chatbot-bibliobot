## Getting Started

### Prerequisites

Ensure you have Python installed. It is recommended to use `miniconda` or `conda` for environment management.

### Installation

1.  **Install Miniconda (if not already installed)**

    Download and install Miniconda from the official website: <mcurl name="Miniconda Installer" url="https://docs.conda.io/en/latest/miniconda.html"></mcurl>

2.  **Create a Conda Environment**

    Open your terminal or Anaconda Prompt and create a new environment:

    ```bash
    conda create -n chatbot-env python=3.9
    conda activate chatbot-env
    ```

3.  **Install Requirements**

    Navigate to the project directory and install the necessary packages:

    ```bash
    cd /path/to/your/chatbot-streamlit-demo
    pip install -r requirements.txt
    ```

4.  **Run the Streamlit Application**

    ```bash
    streamlit run streamlit_app.py
    ```

    The application will open in your web browser.

## Code Structure

- streamlit_app.py: The main Streamlit application file, containing the chatbot UI and logic.
- database_tools.py: Contains functions for interacting with the sales_data.db database.
- requirements.txt: Lists all Python dependencies required for the project.
- streamlit_react_app.py: (Optional) Another Streamlit application, possibly demonstrating React integration.
- streamlit_react_tools_app.py: (Optional) Another Streamlit application, possibly demonstrating React tools integration.

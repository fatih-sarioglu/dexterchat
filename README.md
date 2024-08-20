# DexterChat
DexterChat is a simple AI chat application
designed to help users with their questions. The
app is built using
[Streamlit](https://streamlit.io/),
[LangChain](https://langchain.com/), and
[GPT](https://openai.com/chatgpt).
## Features
- **Real-time AI interaction:** Users can ask
questions and receive responses from the AI in
real-time.
- **Conversation History:** User conversations are
saved and can be retrieved later, thanks to
MongoDB integration.
- **Easy-to-use Interface:** Built with Streamlit,
the app offers a user-friendly and interactive web
interface.
- **Powered by GPT:** The app utilizes OpenAI's
GPT models for natural language processing and
understanding.
## Technologies Used
- **Streamlit:** For building the web interface.
- **LangChain:** For chaining and managing the
flow of language models.
- **GPT:** The core AI model used for generating
responses.
- **MongoDB:** For storing and retrieving user
conversations.
## Installation
To get started with DexterChat, follow these
steps:
1. **Clone the repository:**
   ```bash
   git clone https://github.com/fatih-sarioglu/dexterchat.git
   ```
2. **Navigate to the project directory:**
   ```bash
   cd dexterchat
   ```
3. **Create a `.env` file in the root directory** with the following content:

    ```plaintext
    OPENAI_API_KEY=your-openai-api-key
    MONGODB_URI=your-mongodb-uri
    ```
4. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
## Usage
After installing the dependencies, you can run the
app locally:
```bash
streamlit run app.py
```
## Contributing
Contributions are welcome! If you have any ideas,
feel free to fork the repository and submit a pull
request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
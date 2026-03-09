# Multi-Agent AI Research System

A sophisticated AI-powered research system that automates the entire research-to-publication pipeline using multiple specialized agents. Built with LangGraph and OpenAI's GPT-4o-mini, featuring a modern Streamlit web interface.

## 🚀 Features

- **Multi-Agent Workflow**: 4 specialized agents work in sequence:
  - **Research Agent**: Conducts comprehensive research and gathers key facts
  - **Writer Agent**: Creates well-structured article drafts
  - **Fact-Checker Agent**: Validates claims against research notes
  - **Reviewer Agent**: Produces publication-ready final articles

- **Real-Time Streaming**: Watch the pipeline progress in real-time through the web interface
- **Modern UI**: Sleek, responsive Streamlit interface with dark theme
- **Robust Architecture**: Built on LangGraph for reliable agent orchestration
- **OpenAI Integration**: Powered by GPT-4o-mini for high-quality outputs

## 🛠️ Tech Stack

- **Backend**: Python, LangGraph, LangChain
- **Frontend**: Streamlit
- **AI Model**: OpenAI GPT-4o-mini
- **Environment**: Python 3.8+

## 📦 Installation

1. **Clone or download the project** to your local machine

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API keys**:
   - Create a `.env` file in the `keys/` directory
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```

4. **Run the application**:
   ```bash
   streamlit run frontend/ui.py
   ```

## 🎯 Usage

1. Open the Streamlit app in your browser
2. Enter your research topic in the input field
3. Click "Generate Research Article"
4. Watch the real-time progress as each agent completes its task
5. View the final polished article

### CLI Usage (Optional)

You can also run the backend directly from command line:

```bash
cd backend/src
python main.py "Your research topic here"
```

## ⚙️ Configuration

- **API Key**: Store your OpenAI API key in `keys/.env`
- **Model**: Currently configured for GPT-4o-mini (can be changed in `backend/src/main.py`)
- **Temperature**: Set to 0.7 for creative yet consistent outputs

## 🔧 Troubleshooting

### Common Issues

1. **"Module not found" errors**:
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version (3.8+ required)

2. **OpenAI API errors**:
   - Verify your API key is correct and has sufficient credits
   - Check your `.env` file is in the `keys/` directory

3. **Streamlit not starting**:
   - Ensure you're running from the project root: `streamlit run frontend/ui.py`
   - Check if port 8501 is available

4. **Slow performance**:
   - Each agent makes API calls to OpenAI, so response time depends on API latency
   - Consider upgrading to GPT-4 for faster responses (modify model in `main.py`)

### Development

- Backend code: `backend/src/main.py`
- Frontend code: `frontend/ui.py`
- Dependencies: `requirements.txt`
- Environment variables: `keys/.env`

## 📄 License

This project is open-source. Feel free to modify and distribute.

## 🤝 Contributing

Contributions welcome! Please submit issues and pull requests on GitHub.

---

**Built with ❤️ using LangGraph and Streamlit**</content>
<parameter name="filePath">c:\Users\user\Downloads\Multi-Agent AI Research System\README.md

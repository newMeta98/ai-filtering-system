# 🧠 Example AI Filtering System

A scalable template system for filtering content using AI and customizable rules. Designed for batch processing and adaptable to various use cases (e.g., product moderation, content categorization). 

## ✨ Features
- 🤖 **AI-Powered Filtering**: Integrates with DeepSeek LLM for intelligent analysis
- ⚙️ **Batch Processing**: Handles 50 items/API call (scale to 3000+ items with linear cost/time increase)
- 📚 **Dynamic Knowledge Base**: Use 1-1000+ `.txt` rule files (optimized for 300-500 lines/file. Linear cost/time increase with number of files)
- 🌐 **Web Interface**: Flask-based UI with bulk copy/paste functionality (Bootstrap, user-friendly UI)
- 📊 **Excel Integration**: Export results to/from spreadsheets
- 🎨 **Adaptable Architecture**: Easily modify for spam detection, content sorting, etc.

## 🛠️ Installation
```bash
git clone https://github.com/yourusername/ai-filtering-system.git
cd ai-filtering-system
pip install flask openai pandas python-dotenv
```

## 🔧 Configuration
Environment Setup (.env):

```env
🔑 DEEPSEEK_API_KEY=your_api_key_here
🔒 SECRET_KEY=your_flask_secret
```
## Knowledge Files:

Add .txt files to /knowledge directory (recommended: 1- 20 files. up to 500 lines, it can be fromed in any way AI will know that to do, it dosnt need to be Restricted categories list it can be taxt from a site you coped about restrictes items for example so the from of knowlage dosent matter that much.)

📝 Example rule format:

```txt
❌ Restricted categories:
- 🔫 Weapons
- 🔞 Adult content
- 💰 Counterfeit goods
```
## Input Data:

Add titles to products.txt (1 per line, if you use products.txt leave field in UI empty) or Paste titles in UI (1 per line)

## 🚀 Usage
Web Interface:

```bash
python app.py
```
Visit http://localhost:5000

**📋 Paste titles or use default file**

**🖱️ Click "Filter Products"**

**📋 Copy results using bulk/individual buttons (you can see data in json format in data.json)**

## Excel Processing:

```bash
python helpers.py
```

## 📂 Project Structure

├──  app.py                          # Main application
├──  utils
│    └── 🤖 api_client.py           # AI integration  
├──  📚 knowledge/                   # Rule repository
│    └── 📄 knowledge.txt   
├──  📊 excel/                      # Excel manipulation
│    ├── helpers.py                 # Excel utilities
│    ├── 📄 data.json
│    ├── 📝 allproductsdata.xlsx        
│    └── 📝 allowed_products.xlsx   
├── 🖥️ templates/                   # Web UI
│    └── index.html
├── ⚙️ .env                         # Configuration template
└── 📄 data.json                    # Persistent storage


##📌 Notes
**Firts Run:**
recommended to try with all knowledge files and 20-50 items/titles so you can have small text. With more items and knowlate it will take alot or time of it to be done.

**Scalability:**

⏳ Processing time scales linearly (50 titles/batch)

💸 API costs increase with more knowledge files/titles

🖥️ Add RAM if processing >10,000 items (1-2000 recommended)

**Customization:**

🎨 Change product_filterLLM() in api_client.py for different AI providers

🖌️ Modify index.html for new UI layouts

🔄 Replace knowledge files with domain-specific rules

## 📜 License
MIT License - Free for modification and commercial use. ⚠️ Not responsible for filtering accuracy.
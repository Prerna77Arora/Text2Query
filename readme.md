# 🧠 Natural Language to SQL Interface

Query **any SQLite database** using plain English!  
This project converts natural language to SQL using **LangChain** and **Groq’s LLaMA3 model**, executes the generated SQL against a specified SQLite database, and displays results in a sleek **Streamlit** web interface.

---

## 📁 Project Structure

```
.
├── app.py          # Streamlit app for user interaction
├── database.py     # Optional script to create/populate a sample DB
├── your_database.db# SQLite DB file (user-provided or auto-loaded)
├── requirements.txt
└── README.md
```

---

## 📊 Features

- 💬 Convert English questions into SQL using LLaMA3 via Groq API
- 📂 Support for **any SQLite database**
- 🧠 Auto-extracts and feeds database schema to the LLM
- 📊 View query results in an interactive table
- 📥 Download results as CSV
- 🔍 Toggle to view a plain-English explanation of the SQL
- 📈 Auto-render bar charts for `COUNT`, `AVG`, `SUM` queries

---

## 🔧 How to Adapt for Any Database

To support any SQLite `.db` file:

1. **Replace** the default `student.db` with your own `.db` file
2. In `app.py`, modify the `DB_PATH` variable:

   ```python
   DB_PATH = "your_database.db"
   ```

3. Make sure the schema is readable. The code automatically extracts table/column names using:

   ```sql
   SELECT name FROM sqlite_master WHERE type='table';
   PRAGMA table_info(table_name);
   ```

4. This schema is sent to LLaMA3 to help it generate accurate SQL for your specific database.

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/nl2sql-interface.git
cd nl2sql-interface
```

### 2. Install Dependencies

Create a `requirements.txt` file with:

```txt
streamlit
pandas
langchain
langchain-groq
```

Then install:

```bash
pip install -r requirements.txt
```

### 3. Set Groq API Key

**For Linux/macOS:**

```bash
export GROQ_API_KEY=your_groq_api_key
```

**For Windows (CMD):**

```cmd
set GROQ_API_KEY=your_groq_api_key
```

### 4. Provide Your SQLite Database

- Use `student.db` (provided), or
- Replace it with your own `.db` file and update the `DB_PATH` in `app.py`

### 5. Launch the App

```bash
streamlit run app.py
```

---

## 🔍 Example Natural Language Queries

Try questions like:

- "How many records are there in each table?"
- "Show all entries from the `employees` table."
- "What is the average salary by department?"
- "List customers who spent more than $500."

---

## 🧰 Tech Stack

- **Python 3.7+**
- **SQLite** – lightweight relational database
- **Streamlit** – frontend UI
- **LangChain** – framework for LLM chaining
- **Groq + LLaMA3** – LLM backend for NL→SQL

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgements

Thanks to these amazing tools:

- [LangChain](https://www.langchain.com/)
- [Groq](https://groq.com/)
- [Streamlit](https://streamlit.io/)

---

> ✨ Build once, query any database with the power of language + LLMs!

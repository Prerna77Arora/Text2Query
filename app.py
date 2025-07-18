import os
import sqlite3
import pandas as pd
import streamlit as st

from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


# Convert natural language to SQL query
def get_sql_query(user_query):
    prompt = ChatPromptTemplate.from_template("""
You are an expert in converting English to SQL queries.
The SQL database is called STUDENT with columns: NAME, COURSE, SECTION, MARKS.

Rules:
- Only output the SQL query.
- Do NOT include commentary, backticks, or phrases like "Here is the SQL:".
- Do NOT explain anything.
- End the output with a semicolon.

Examples:
- "How many entries of records are present?" → SELECT COUNT(*) FROM STUDENT;
- "Tell me all the students studying in Data Science COURSE?" → 
  SELECT * FROM STUDENT WHERE COURSE = "Data Science";

Now, convert this English question into a valid SQL query: {user_query}
""")

    llm = ChatGroq(
        groq_api_key=os.environ.get("GROQ_API_KEY"),
        model_name="llama3-8b-8192"
    )

    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"user_query": user_query})


# Get a simple explanation of the SQL query
def explain_sql(sql_query):
    explanation_prompt = ChatPromptTemplate.from_template("""
        You are an assistant that explains SQL queries in simple terms.
        Explain this query briefly: {sql_query}
    """)
    llm = ChatGroq(
        groq_api_key=os.environ.get("GROQ_API_KEY"),
        model_name="llama3-8b-8192"
    )
    chain = explanation_prompt | llm | StrOutputParser()
    return chain.invoke({"sql_query": sql_query})


# Execute SQL and return result and column headers
def return_sql_response(sql_query):
    database = "student.db"
    with sqlite3.connect(database) as conn:
        cursor = conn.execute(sql_query)
        data = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        return data, columns


# Render a bar chart if appropriate
def render_bar_chart(df):
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    if len(numeric_cols) >= 1 and 'COURSE' in df.columns:
        st.subheader("📊 Chart View (Grouped by COURSE)")
        st.bar_chart(data=df, x="COURSE", y=numeric_cols[0])


# Main Streamlit app
def main():
    st.set_page_config(page_title="Text To SQL", page_icon="🧠", layout="centered")
    st.title("🧠 Natural Language to SQL Interface")

    with st.form("query_form"):
        user_query = st.text_input("Enter your question:", placeholder="e.g. What is the average marks per course?")
        submitted = st.form_submit_button("Generate SQL & Fetch Results")

    if submitted and user_query:
        with st.spinner("Processing..."):
            try:
                # Convert user query to SQL
                sql_query = get_sql_query(user_query)
                data, columns = return_sql_response(sql_query)

                st.success("✅ SQL Query Generated")
                st.code(sql_query, language="sql")

                # Optional: SQL explanation
                if st.toggle("Show SQL Explanation 📝"):
                    explanation = explain_sql(sql_query)
                    st.info(explanation)

                # Display results
                if data:
                    df = pd.DataFrame(data, columns=columns)
                    st.subheader("📊 Query Results:")
                    st.dataframe(df, use_container_width=True)

                    # CSV download
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="⬇️ Download results as CSV",
                        data=csv,
                        file_name='query_results.csv',
                        mime='text/csv'
                    )

                    # Show chart if applicable
                    if any(keyword in sql_query.upper() for keyword in ["AVG", "SUM", "COUNT"]):
                        render_bar_chart(df)
                else:
                    st.warning("No data returned for this query.")

            except Exception as e:
                st.error(f"❌ Error: {e}")

if __name__ == '__main__':
    main()

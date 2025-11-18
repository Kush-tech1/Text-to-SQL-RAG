import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts.prompt import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.example_selectors.semantic_similarity import SemanticSimilarityExampleSelector
from few_shots import few_shots

# -----------------------------
# 1️⃣ Streamlit page setup
# -----------------------------
st.set_page_config(page_title="NL → SQL Generator", layout="wide")
st.title("💻 Natural Language → SQL Generator")
st.markdown("Ask any question about your MySQL database and get executable SQL queries!")

user_question = st.text_area("Enter your question:")

# -----------------------------
# 2️⃣ Cached initializations
# -----------------------------
@st.cache_resource
def init_llm():
    os.environ["GOOGLE_API_KEY"] = "AIzaSyCza6QCUans78f0tEFUI1oEnuQTm9Q7Sf8"
    return ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

@st.cache_resource
def init_db():
    db_uri = "mysql+pymysql://root:root@localhost/atliq_tshirts"
    return SQLDatabase.from_uri(db_uri, sample_rows_in_table_info=3)

@st.cache_resource
def init_vectorstore(few_shots):
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    vectorstore = Chroma.from_texts(
        [" ".join(ex.values()) for ex in few_shots],
        embeddings,
        metadatas=few_shots
    )
    return vectorstore

@st.cache_resource
def init_example_selector(few_shots):
    vectorstore = init_vectorstore(few_shots)
    return SemanticSimilarityExampleSelector(vectorstore=vectorstore, k=2)

def format_selected_examples(examples):
    formatted = ""
    for ex in examples:
        formatted += f"USER QUESTION: {ex['User Question']}\nSQL QUERY:\n{ex['SQL Query']}\n\n"
    return formatted

def clean_sql(sql_text):
    # Remove markdown code fences and extra whitespace
    sql_text = sql_text.replace("```sql", "").replace("```", "")
    return sql_text.strip()

prompt = PromptTemplate(
    template="""
You are an expert MySQL query generator.

Your goal: Given a database schema and a natural-language question, generate a single, correct, and executable MySQL query.

RULES:
1. Use ONLY the columns and tables provided in the schema.
2. Do NOT invent or assume new fields, tables, or relationships.
3. Always use MySQL syntax (not SQLite or PostgreSQL).
4. Never include explanations, natural language, or markdown code fences (no ```sql).
5. Return ONLY the raw SQL query.
6. Prefer readable aliases and JOINs.
7. If filters are implied (e.g. “this month”), translate them correctly 
   (e.g. `WHERE MONTH(date) = MONTH(CURDATE()) AND YEAR(date) = YEAR(CURDATE())`).
8. Avoid ambiguous columns — qualify with table names if needed.

DATABASE SCHEMA:
{schema}

FEW-SHOT EXAMPLES:
{few_shots}

USER QUESTION:
{question}

OUTPUT (Only SQL):
""",
    input_variables=["schema", "few_shots", "question"]
)

# -----------------------------
# 6️⃣ LCEL pipeline
# -----------------------------
def run_pipeline(user_question):
    db = init_db()
    llm = init_llm()
    example_selector = init_example_selector(few_shots)

     # Build prompt manually (required to display it)
    final_prompt = prompt.format(
        schema=db.get_table_info(),
        few_shots=format_selected_examples(
            example_selector.select_examples({"Question": user_question})
        ),
        question=user_question
    )

    # Show the prompt
    st.code(final_prompt)

    chain = (
        {
            "schema": lambda _: db.get_table_info(),
            "few_shots": lambda x: format_selected_examples(
                example_selector.select_examples({"Question": x["question"]})
            ),
            "question": lambda x: x["question"]
        }
        | prompt
        | llm
    )

    sql = chain.invoke({"question": user_question}).content
    return clean_sql(sql)


# -----------------------------
# 7️⃣ Run query and show results
# -----------------------------
if st.button("Generate SQL") and user_question.strip():
    with st.spinner("Generating SQL..."):
        try:
            sql_query = run_pipeline(user_question)
            st.subheader("Generated SQL:")
            st.code(sql_query, language="sql")
        except Exception as e:
            st.error(f"Error: {e}")

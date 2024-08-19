# InsightPro-Financial-News-Research-Assistant

InsightPro is a Streamlit-based application designed to assist equity research analysts and financial professionals in aggregating and analyzing financial news articles. By leveraging the power of AI, this tool automates the research process, helping you derive actionable insights from vast amounts of content in a fraction of the time.

### Features
Automated News Aggregation: Automatically fetch and process financial articles from reliable sources using web scraping techniques.
Embeddings & Vector Storage: Convert articles into embeddings with OpenAIEmbeddings and store them efficiently using FAISS for fast and accurate retrieval.
Advanced Question Answering: Query processed articles with complex financial questions, and receive context-aware responses powered by GPT-4 through ChatOpenAI.
Source Transparency: Display sources alongside answers, allowing users to verify the information and ensure accuracy.
Cost Optimization: Efficient use of API calls by minimizing redundant requests and utilizing FAISS to store and retrieve relevant data.

### Architecture Overview
Web Scraping: Extract content from trustworthy financial news websites using web scrapers. These scrapers can be scheduled to run periodically (e.g., every 1-2 hours) to keep your data up-to-date.
Text Splitting: The fetched articles are split into smaller chunks using RecursiveCharacterTextSplitter from Langchain, ensuring optimal processing.
Embeddings & FAISS Vector Store: Convert text chunks into high-dimensional embeddings with OpenAIEmbeddings and store them in a FAISS vector database for efficient similarity search and retrieval.
Retrieval-Based QA: Use RetrievalQAWithSourcesChain to query the FAISS vector store, fetch the most relevant chunks, and pass them to the language model for generating responses.
GPT-4 Powered Responses: Leverage GPT-4 through ChatOpenAI to generate insightful and accurate answers to financial queries based on the processed articles.

### Usage
Enter URLs: Input the URLs of the financial articles you want to analyze.
Process Data: Click the "Process URLs" button to load and process the articles.
Ask Questions: Once the data is processed, type your financial questions into the input box, and InsightPro will provide you with accurate and context-driven answers.
View Sources: Verify the answers by reviewing the sources displayed alongside the responses.

### Challenges & Solutions
Token Limits: Implemented a MapReduce approach to handle long articles by splitting them into smaller chunks and processing them efficiently.
Cost Management: Optimized the use of OpenAI’s API by leveraging FAISS for vector storage, reducing redundant API calls, and ensuring cost-effective analysis.
Efficient Information Retrieval: Used FAISS to find semantic similarity between queries and stored data, allowing for accurate retrieval of relevant information from large articles.

### Future Scope
Enhanced Web Scraping: Add support for more financial news websites and automate the web scraping process to update the database frequently.
Interactive Chatbot Interface: Develop a more interactive chatbot UI for real-time financial queries and responses.
Integration with Financial Databases: Extend functionality to include direct integration with financial data sources (e.g., stock market data, financial reports).
Scalability Improvements: Implement distributed processing to handle larger datasets and more complex queries as the application scales.

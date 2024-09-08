import re
from collections import defaultdict
import streamlit as st

# Function to tokenize text
def tokenize(text):
    return set(re.findall(r'\b\w+\b', text.lower()))

# Function to build the inverted index
def build_inverted_index(docs):
    index = defaultdict(set)
    for doc_id, text in docs.items():
        words = tokenize(text)
        for word in words:
            index[word].add(doc_id)
    return index

# Function to perform Boolean retrieval
def boolean_retrieval(index, query):
    query = query.lower()
    
    if ' and ' in query:
        subqueries = query.split(' and ')
        result_docs = set(index.get(subqueries[0].strip(), set()))
        for subquery in subqueries[1:]:
            subquery = subquery.strip()
            result_docs = result_docs.intersection(index.get(subquery, set()))
    
    elif ' or ' in query:
        subqueries = query.split(' or ')
        result_docs = set()
        for subquery in subqueries:
            subquery = subquery.strip()
            result_docs = result_docs.union(index.get(subquery, set()))
    
    elif ' not ' in query:
        subqueries = query.split(' not ')
        if len(subqueries) == 2:
            term_to_exclude = subqueries[1].strip()
            include_terms = subqueries[0].strip()
            result_docs = set(index.get(include_terms, set()))
            result_docs = result_docs.difference(index.get(term_to_exclude, set()))
    
    else:
        tokens = re.findall(r'\b\w+\b', query)
        result_docs = set()
        for token in tokens:
            result_docs = result_docs.union(index.get(token, set()))
    
    return result_docs

# Streamlit app
def main():
    st.title("Boolean Information Retrieval System")

    # File upload
    uploaded_files = st.file_uploader("Upload documents", type="txt", accept_multiple_files=True)
    
    # Check if any files are uploaded
    if uploaded_files:
        documents = {}
        doc_ids = {}
        for idx, uploaded_file in enumerate(uploaded_files):
            content = uploaded_file.read().decode("utf-8")
            doc_id = f"Document {idx + 1}"  # Use numerical ID for the document
            documents[doc_id] = content
            doc_ids[uploaded_file.name] = doc_id  # Map original file names to new document IDs
        
        # Build the inverted index
        inverted_index = build_inverted_index(documents)
        
        # User query input
        query = st.text_input("Enter your Boolean query (supports AND, OR, NOT):")
        
        # Submit button
        if st.button("Submit"):
            if query:
                # Perform search
                results = boolean_retrieval(inverted_index, query)
                
                # Display results
                if results:
                    for doc_id in results:
                        st.write(f"**{doc_id}:**")
                        # Display a preview of the document
                        preview = documents[doc_id][:500]  # First 500 characters
                        st.write(preview + ("..." if len(documents[doc_id]) > 500 else ""))
                        st.write("---")  # Separator between documents
                else:
                    st.write("No documents found matching the query.")
            else:
                st.write("Please enter a query.")
    
    else:
        st.write("Please upload some text files to search through.")

if __name__ == "__main__":
    main()

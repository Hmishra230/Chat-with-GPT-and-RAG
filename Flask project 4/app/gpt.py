from transformers import pipeline
import PyPDF2

def get_gpt_response(prompt, retrieved_content=None):
    """
    Generates a response using GPT, optionally augmenting the prompt with retrieved content.
    """
    generator = pipeline("text-generation", model="gpt2")

    if retrieved_content:
        # Combine retrieved content with the user query
        prompt = f"Here is some relevant information: {retrieved_content}\n\nUser Query: {prompt}\n\nAnswer based on the above information:"

    result = generator(prompt, max_new_tokens=100, num_return_sequences=1)  # Generate 100 tokens
    return result[0]['generated_text']


def retrieve_relevant_content(filepath, query):
    """
    Extracts text from a PDF file and finds the most relevant content for the query.
    """
    content = ''

    # Read PDF content
    if filepath.endswith('.pdf'):
        try:
            with open(filepath, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                content = ' '.join(page.extract_text() for page in reader.pages)
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return ''

    # If no content was extracted, return an empty string
    if not content.strip():
        return ''

    # Simplified keyword-based retrieval
    query_words = set(query.lower().split())
    content_words = set(content.lower().split())
    common_words = query_words.intersection(content_words)

    # If common words are found, return relevant content, otherwise return empty string
    if len(common_words) > 0:
        return content[:2000]  # Return the first 2000 characters (or a relevant slice)
    return ''

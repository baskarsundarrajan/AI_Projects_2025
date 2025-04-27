# from utils.pdf_vectorizer import PDFVectorizer
# from utils.vector_operations import VectorDBOperations as db
# from generate_questions import generate_questions

# # jinaai/jina-embeddings-v2-base-en

# if __name__ == "__main__":
#     pdf = PDFVectorizer()
#     chunks = pdf.pdf_vectorize_store()
#     try:
#         with db.connect_weaviate() as client:
#             # db.insert(client,"pdf_chunks", chunks, "user_id")
#             # client.delete("pdf_chunk")
#             res = generate_questions(client)
#             # print(res)
#         # del client
#     except Exception as e:
#         print("error",e)
#         exit(0)

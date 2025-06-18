from langchain_core.tools import tool
from documents.models import Document


@tool
def list_documents():
    """Get documents for the current user"""
    qs = Document.objects.filter(active=True)
    response_data = []
    for document in qs:
        response_data.append({
            "id": document.id,
            "title": document.title,
        })
    return response_data


@tool
def get_document(document_id: int):
    """Get the details of a document by id"""
    document = Document.objects.get(id=document_id, active=True)
    response_data = {
            "id": document.id,
            "title": document.title,
        }
    return response_data

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from documents.models import Document


@tool
def list_documents(config: RunnableConfig):
    """List the most recent 5 documents for the current user"""
    limit = 5
    metadata = config.get('configurable') or config.get('metadata')
    user_id = metadata.get('user_id')

    qs = Document.objects.filter(owner_id=user_id, active=True).order_by("-created_at")
    response_data = []
    for document in qs[:limit]:
        response_data.append({
            "id": document.id,
            "title": document.title,
        })
    return response_data


@tool
def get_document(config: RunnableConfig, document_id: int):
    """Get the details of a document by id"""
    metadata = config.get('configurable') or config.get('metadata') 
    user_id = metadata.get('user_id')
    try:
        document = Document.objects.get(id=document_id, owner_id=user_id, active=True)
    except Document.DoesNotExist:
        return Exception("Document not found, try again")
    except Exception:
        return Exception("Invalid request for a document details not found, try again")
    response_data = {
            "id": document.id,
            "title": document.title,
        }
    return response_data


document_tools = [
    list_documents,
    get_document,
]

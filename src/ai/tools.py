from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from documents.models import Document


@tool
def list_documents(config: RunnableConfig):
    """Get documents for the current user"""
    print(config)
    metadata = config.get('metadata') or config.get('configurable')
    user_id = metadata.get('user_id')
    qs = Document.objects.filter(owner_id=user_id, active=True)
    response_data = []
    for document in qs:
        response_data.append({
            "id": document.id,
            "title": document.title,
        })
    return response_data


@tool
def get_document(config: RunnableConfig, document_id: int):
    """Get the details of a document by id"""
    metadata = config.get('metadata') or config.get('configurable')
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

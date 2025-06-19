from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from documents.models import Document
from django.db.models import Q


@tool
def search_query_documents(config: RunnableConfig, query: str, limit: int = 5):
    """Search the most recent LIMIT documents for the current user  with maximum of 25.

    arguments:
    query: string or lookup search across title or content of document
    limit: number of results"""
    if limit > 25:
        limit = 25

    metadata = config.get('configurable') or config.get('metadata')
    user_id = metadata.get('user_id')

    default_lookups = {
        "active": True,
        "owner_id": user_id,
    }

    qs = Document.objects.filter(**default_lookups).filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).order_by("-created_at")
    response_data = []
    for document in qs[:limit]:
        response_data.append({
            "id": document.id,
            "title": document.title,
        })
    return response_data


@tool
def list_documents(config: RunnableConfig):
    """List the most recent 5 documents for the current user"""
    limit = 5
    metadata = config.get('configurable') or config.get('metadata')
    user_id = metadata.get('user_id')

    qs = Document.objects.filter(
        owner_id=user_id, active=True).order_by("-created_at")
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
        document = Document.objects.get(
            id=document_id, owner_id=user_id, active=True)
    except Document.DoesNotExist:
        return Exception("Document not found, try again")
    except Exception:
        return Exception("Invalid request for a document details not found, try again")
    response_data = {
        "id": document.id,
        "title": document.title,
    }
    return response_data


@tool
def create_document(config: RunnableConfig, title: str, content: str):
    """ Create a new document for the current user

    Args:
        config (RunnableConfig): RunnableConfig object
        title (str): document title
        content (str): content of the document

    Returns:
        dict: document details
    """
    metadata = config.get('configurable') or config.get('metadata')
    user_id = metadata.get('user_id')

    if user_id is None:
        raise Exception("Invalid request for user")

    try:
        document = Document.objects.create(
            owner_id=user_id, title=title, content=content, active=True)
    except Exception:
        return Exception("Invalid request to create document, try again")

    response_data = {
        "id": document.id,
        "title": document.title,
        "content": document.content,
        "created_at": document.created_at,
        "updated_at": document.updated_at,
        "active": document.active,
    }
    return response_data


@tool
def delete_document(config: RunnableConfig, document_id: int):
    """Delete a document by id"""
    metadata = config.get('configurable') or config.get('metadata')
    user_id = metadata.get('user_id')

    if user_id is None:
        raise Exception("Invalid request for user")

    try:
        doc_obj = Document.objects.get(
            id=document_id, owner_id=user_id, active=True)
    except Document.DoesNotExist:
        raise ("Document not found, try again")
    except Exception:
        raise Exception(
            "Invalid request for a document details not found, try again")

    doc_obj.delete()
    response_data = {"message": "Document deleted successfully"}
    return response_data


@tool
def update_document(config: RunnableConfig, document_id: int, title: str = None, content: str = None):
    """ updae a document for the current user

    Args:
        config (RunnableConfig): RunnableConfig object
        document_id (int): document id
        title (str): document title
        content (str): content of the document

    Returns:
        dict: document details
    """
    metadata = config.get('configurable') or config.get('metadata')
    user_id = metadata.get('user_id')

    if user_id is None:
        raise Exception("Invalid request for user")

    try:
        doc_obj = Document.objects.get(
            id=document_id, owner_id=user_id, active=True)
    except Document.DoesNotExist:
        raise ("Document not found, try again")
    except Exception:
        raise Exception(
            "Invalid request for a document details not found, try again")

    if title is not None:
        doc_obj.title = title
    if content is not None:
        doc_obj.content = content

    if title or content:
        doc_obj.active = True
        doc_obj.save()

    response_data = {
        "id": doc_obj.id,
        "title": doc_obj.title,
        "content": doc_obj.content,
        "created_at": doc_obj.created_at,
        "updated_at": doc_obj.updated_at,
        "active": doc_obj.active,
    }
    return response_data


document_tools = [
    list_documents,
    get_document,
    create_document,
    delete_document,
    update_document,
    search_query_documents
]

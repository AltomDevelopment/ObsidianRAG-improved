# create_embeddings/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Document
from .forms import DocumentForm

def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save()
            return redirect('upload_success', pk=doc.pk)
    else:
        form = DocumentForm()
    return render(request, 'create_embeddings/upload.html', {'form': form})

def upload_success(request, pk):
    return render(request, 'create_embeddings/delayed_redirect.html', {'pk': pk})

def parse_document(request, pk):
    if request.user.is_authenticated:
        if getattr(request.user, 'is_admin', False):
            document = get_object_or_404(Document, pk=pk)
            return render(request, 'create_embeddings/parse_document.html', {
                'document': document,
                'uploadPDF': document.uploadPDF
            })
        else:
            messages.error(request, 'You do not have permission to view this document.')
            return redirect('unauthorized')  # You should define this route or template
    else:
        return redirect('login')  # Django's built-in login view

\n\n# --- Semantic Search View ---\nfrom django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from create_embeddings.models import Document
from rag_pipeline import semantic_search, embed_and_store
import os

@csrf_exempt
def search_documents(request):
    if request.method == "POST":
        query = request.POST.get("query", "")
        if not query:
            return JsonResponse({"error": "Query is required"}, status=400)
        results = semantic_search(query)
        return JsonResponse({"results": results})
    return render(request, "create_embeddings/search.html")
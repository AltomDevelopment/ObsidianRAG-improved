# create_embeddings/urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path("upload/", views.upload_document, name="upload_document"),
    path("upload/success/<int:pk>/", views.upload_success, name="upload_success"),
    path("parse/<int:pk>/", views.parse_document, name="parse_document"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
\n\n# --- Semantic Search URL ---\nfrom django.urls import path
from . import views

urlpatterns = [
    path("search/", views.search_documents, name="semantic_search"),
]
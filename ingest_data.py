import os
import shutil
from src.services.vector_store import VectorStoreService
from src.core.config import settings

def rebuild_knowledge_base():
    faq_path = os.path.join("data", "faq.txt")
    db_path = settings.vector_db_path

    print(f"--- Start indexating ---")

    if os.path.exists(db_path):
        print(f"Remove old database at path: {db_path}...")
        shutil.rmtree(db_path)

    if not os.path.exists(faq_path):
        print(f"Error: File {faq_path} not found! Create before starting script.")
        return

    try:
        service = VectorStoreService()
        service.build_index(faq_path)
        print(f"Success: DataBase saved at path - {db_path}")
    except Exception as e:
        print(f"Error at indexating: {e}")

if __name__ == "__main__":
    rebuild_knowledge_base()
from pathlib import Path


DOCUMENT_METADATA = {
    "employee_handbook.txt": {
        "department": "General",
        "document_type": "Handbook",
    },
    "leave_policy.txt": {
        "department": "HR",
        "document_type": "Policy",
    },
    "contractor_policy.txt": {
        "department": "HR",
        "document_type": "Policy",
    },
    "remote_work_policy.txt": {
        "department": "HR",
        "document_type": "Policy",
    },
    "it_security_policy.txt": {
        "department": "IT",
        "document_type": "Policy",
    },
}


def load_documents(data_dir: str | Path) -> list[dict]:
    """
    Load all .txt documents from the data directory.

    Returns:
        List of dictionaries containing document text and metadata.
    """

    data_path = Path(data_dir)

    if not data_path.exists():
        raise FileNotFoundError(
            f"Data directory does not exist: {data_dir}"
        )

    documents = []

    for file_path in sorted(data_path.glob("*.txt")):
        text = file_path.read_text(
            encoding="utf-8"
        ).strip()

        if not text:
            continue

        metadata = DOCUMENT_METADATA.get(
            file_path.name,
            {
                "department": "Unknown",
                "document_type": "Unknown",
            },
        )

        document = {
            "text": text,
            "metadata": {
                "source": file_path.name,
                "department": metadata["department"],
                "document_type": metadata["document_type"],
                "status": "active",
            },
        }

        documents.append(document)

    return documents
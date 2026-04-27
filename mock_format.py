import json
import zipfile
from datetime import datetime
from pathlib import Path

from db import Database


def export_mock(db: Database, mock_id: str, file_path: str) -> bool:
    try:
        mock = db.get_mock(mock_id)
        questions = db.get_questions(mock_id)
        if not mock:
            return False
        target = Path(file_path)
        if target.suffix.lower() != ".jmock":
            target = target.with_suffix(".jmock")
        manifest = {
            "version": "1.0",
            "app": "jee-mock-app",
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }
        payload = {"mock": mock, "questions": questions}
        with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("manifest.json", json.dumps(manifest, indent=2))
            archive.writestr("questions.json", json.dumps(payload, indent=2))
            archive.writestr("images/", "")
        return True
    except Exception as exc:
        print(f"export_mock error: {exc}")
        return False


def import_mock(db: Database, file_path: str) -> str:
    try:
        with zipfile.ZipFile(file_path, "r") as archive:
            manifest = json.loads(archive.read("manifest.json").decode("utf-8"))
            if manifest.get("app") != "jee-mock-app" or manifest.get("version") != "1.0":
                raise ValueError("Unsupported .jmock file")
            payload = json.loads(archive.read("questions.json").decode("utf-8"))

        mock = payload.get("mock", {})
        original_id = mock.get("id")
        if original_id and db.mock_exists(original_id):
            return original_id

        mock["source"] = "imported"
        new_mock_id = db.insert_mock_record(mock)
        if not new_mock_id:
            return ""

        for question in payload.get("questions", []):
            question["mock_id"] = new_mock_id
            db.insert_question_record(question, new_mock_id)
        return new_mock_id
    except Exception as exc:
        print(f"import_mock error: {exc}")
        return ""

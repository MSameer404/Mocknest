import json
import re
import zipfile
from datetime import datetime
from pathlib import Path

from db import Database

IMAGES_DIR = Path.home() / ".jee_mock_app" / "images"
IMAGES_DIR.mkdir(parents=True, exist_ok=True)


def _process_export_images(text: str, archive: zipfile.ZipFile, added_images: set) -> str:
    if not text:
        return text
    
    def repl(match):
        alt_text = match.group(1)
        filepath = match.group(2)
        try:
            path_obj = Path(filepath)
            if path_obj.exists() and path_obj.is_file():
                filename = path_obj.name
                if filename not in added_images:
                    archive.write(path_obj, f"images/{filename}")
                    added_images.add(filename)
                return f"![{alt_text}](images/{filename})"
        except Exception:
            pass
        return match.group(0)

    return re.sub(r"!\[(.*?)\]\((.*?)\)", repl, text)


def _process_import_images(text: str) -> str:
    if not text:
        return text
    
    def repl(match):
        alt_text = match.group(1)
        filepath = match.group(2)
        if filepath.startswith("images/"):
            filename = filepath.replace("images/", "", 1)
            local_path = IMAGES_DIR / filename
            return f"![{alt_text}]({local_path.as_posix()})"
        return match.group(0)

    return re.sub(r"!\[(.*?)\]\((.*?)\)", repl, text)


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
        
        with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
            added_images = set()
            archive.writestr("images/", "")
            
            for q in questions:
                q["text"] = _process_export_images(q.get("text", ""), archive, added_images)
                options = q.get("options")
                if options:
                    if isinstance(options, str):
                        try:
                            opt_list = json.loads(options)
                            opt_list = [_process_export_images(o, archive, added_images) for o in opt_list]
                            q["options"] = json.dumps(opt_list)
                        except Exception:
                            q["options"] = _process_export_images(options, archive, added_images)
                    elif isinstance(options, list):
                        opt_list = [_process_export_images(o, archive, added_images) for o in options]
                        q["options"] = json.dumps(opt_list)
            
            payload = {"mock": mock, "questions": questions}
            archive.writestr("manifest.json", json.dumps(manifest, indent=2))
            archive.writestr("questions.json", json.dumps(payload, indent=2))
            
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
                
            for item in archive.namelist():
                if item.startswith("images/") and len(item) > len("images/"):
                    filename = item.replace("images/", "", 1)
                    dest_path = IMAGES_DIR / filename
                    with open(dest_path, "wb") as f:
                        f.write(archive.read(item))
                        
            payload = json.loads(archive.read("questions.json").decode("utf-8"))

        mock = payload.get("mock", {})
        questions = payload.get("questions", [])
        
        if len(questions) != 75:
            print("import_mock error: Invalid mock format. Must contain exactly 75 questions.")
            return ""

        original_id = mock.get("id")
        if original_id and db.mock_exists(original_id):
            return original_id

        mock["source"] = "imported"
        new_mock_id = db.insert_mock_record(mock)
        if not new_mock_id:
            return ""

        for question in questions:
            question["mock_id"] = new_mock_id
            question["text"] = _process_import_images(question.get("text", ""))
            
            options = question.get("options")
            if options:
                if isinstance(options, str):
                    try:
                        opt_list = json.loads(options)
                        opt_list = [_process_import_images(o) for o in opt_list]
                        question["options"] = json.dumps(opt_list)
                    except Exception:
                        question["options"] = _process_import_images(options)
                elif isinstance(options, list):
                    opt_list = [_process_import_images(o) for o in options]
                    question["options"] = json.dumps(opt_list)
            
            db.insert_question_record(question, new_mock_id)
            
        return new_mock_id
    except Exception as exc:
        print(f"import_mock error: {exc}")
        return ""

import os
import sys
import json
import hashlib
from datetime import datetime

STATE_FILE = "file_states.json"

class FileChangeDetector:
    def __init__(self, state_filepath=STATE_FILE):
        self.state_filepath = state_filepath
        self.states = self._load_states()

    def _load_states(self):
        if os.path.exists(self.state_filepath):
            try:
                with open(self.state_filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def _save_states(self):
        with open(self.state_filepath, 'w', encoding='utf-8') as f:
            json.dump(self.states, f, indent=4, ensure_ascii=False)

    def calculate_sha256(self, filepath):
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def check_file(self, filepath):
        absolute_path = os.path.abspath(filepath)
        
        if not os.path.exists(absolute_path):
            print("Błąd: Podany plik nie istnieje.")
            return None

        current_hash = self.calculate_sha256(absolute_path)
        current_time = datetime.now().isoformat()

        if absolute_path not in self.states:
            self.states[absolute_path] = {
                "hash": current_hash,
                "timestamp": current_time
            }
            self._save_states()
            return "nie zmieniło się"

        saved_hash = self.states[absolute_path]["hash"]

        if current_hash == saved_hash:
            return "nie zmieniło się"
        else:
            self.states[absolute_path] = {
                "hash": current_hash,
                "timestamp": current_time
            }
            self._save_states()
            return "zmieniło się"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Sposób użycia: python file_monitor.py <ścieżka_do_pliku>")
        sys.exit(1)

    target_file = sys.argv[1]
    detector = FileChangeDetector()
    result = detector.check_file(target_file)
    if result:
        print(result)
import csv
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from characters.models import CharacterClass


class Command(BaseCommand):
    help = "Import D&D classes from CSV into CharacterClass."

    def handle(self, *args, **options):
        csv_path = Path(__file__).resolve().parents[2] / "data" / "classes.csv"

        if not csv_path.exists():
            raise CommandError(f"CSV file not found: {csv_path}")

        created = 0

        with csv_path.open("r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                raise CommandError("classes.csv has no header row.")

            # Your CSV uses "Class"
            # We'll find it case-insensitively
            header_map = {h.lower(): h for h in reader.fieldnames}
            class_col = header_map.get("class")
            if not class_col:
                raise CommandError(f"Could not find 'Class' column. Headers: {reader.fieldnames}")

            for row in reader:
                name = (row.get(class_col) or "").strip()
                if not name:
                    continue
                CharacterClass.objects.get_or_create(char_class_name=name)
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Imported classes from {csv_path}"))
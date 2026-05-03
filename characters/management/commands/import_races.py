import csv
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from characters.models import CharacterRace


class Command(BaseCommand):
    help = "Import races from CSV into CharacterRace."

    def handle(self, *args, **options):
        csv_path = Path(__file__).resolve().parents[2] / "data" / "races.csv"

        if not csv_path.exists():
            raise CommandError(f"CSV file not found: {csv_path}")

        with csv_path.open("r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                raise CommandError("races.csv has no header row.")

            header_map = {h.lower(): h for h in reader.fieldnames}
            races_col = header_map.get("races")
            if not races_col:
                raise CommandError(f"Could not find 'Races' column. Headers: {reader.fieldnames}")

            for row in reader:
                name = (row.get(races_col) or "").strip()
                if not name:
                    continue
                CharacterRace.objects.get_or_create(char_race_name=name)

        self.stdout.write(self.style.SUCCESS(f"Imported races from {csv_path}"))
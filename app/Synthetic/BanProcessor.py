import requests
import yaml
from pathlib import Path
import json


class BanProcessor:
    def __init__(self):
        self.globally_ignored = "https://raw.githubusercontent.com/ufal/olimpic-icdar24/master/app/datasets/splits/annotation_problematic_scores.yaml"
        self.banned_scores = []
        self.banned_pages = []
        with open("app/Synthetic/banned_scores.yaml", "r") as f:
            self.banned_scores = yaml.safe_load(f)

        with open("app/Synthetic/banned_pages.yaml", "r") as f:
            self.banned_pages = yaml.safe_load(f)

    def is_banned_document(self, score_path: Path):
        stripped = self._strip_path(score_path)
        return int(stripped.split("-")[0]) in self.banned_scores

    def is_banned_page(self, page_path: Path):
        return self._strip_path(page_path) in self.banned_pages

    @staticmethod
    def _strip_path(path: Path):
        return path.parts[-1].split(".")[0].replace("lc", "")

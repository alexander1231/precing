import re
import uuid
from typing import Dict
import requests
from dataclasses import dataclass, field
from bs4 import BeautifulSoup
from models.model import Model


@dataclass(eq=False)
class Item(Model):
    collection: str = field(init=False, default="items")
    url: str
    tag_name: str
    query: Dict
    price: float = field(default=None)
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    # def __post_init__(self):
    #     self.price = None

    # def __repr__(self):
    #     return '<Item %s>' % self.url

    def load_price(self) -> float:
        response = requests.get(self.url)
        content = response.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(self.tag_name, self.query)
        string_price = element.text.strip()

        pattern = re.compile(r"(\d+,?\d+\.\d\d)")
        match = pattern.search(string_price)
        found_price = match.group(1)
        without_comas = found_price.replace(",", "")
        self.price = float(without_comas)
        return self.price

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "url": self.url,
            "tag_name": self.tag_name,
            "price": self.price,
            "query": self.query,
        }

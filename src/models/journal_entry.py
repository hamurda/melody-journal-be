from enum import Enum
from typing import List
from pydantic import BaseModel, Field

class Tag(Enum):
    PRACTICE = "Practice"
    TECHNIQUE_BUILDER = "Technique Builder"
    FINGER_GYM = "Finger Gym"
    REPERTOIRE = "Repertoire"
    SIGHTREADING = "Sight-reading"
    WARM_UP = "Warm Up"

class JournalEntry(BaseModel):
    user_id : str
    timestamp : int
    entry_id : str
    content: str = None
    tags: List[Tag] = Field(default_factory=lambda:[Tag.PRACTICE, Tag.REPERTOIRE])

    def to_ddb_dict(self):
        return {
            "UserId": {"S": self.user_id},
            "Timestamp": {"N": str(self.timestamp)},
            "EntryId": {"S": self.entry_id},
            "Entry": {"S": self.content},
            "Tags": {"SS": [tag.value for tag in self.tags]},
        }
    
    def from_ddb_dict_to_dto(item):
        return {
            "EntryId": item["EntryId"]["S"],
            "UserId": item["UserId"]["S"],
            "Timestamp": int(item["Timestamp"]["N"]),
            "Entry": item["Entry"]["S"],
            "Tags": item["Tags"]["SS"]
        }
    
    def __str__(self):
        return self.model_dump_json()
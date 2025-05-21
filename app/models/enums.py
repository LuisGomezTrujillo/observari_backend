from enum import Enum

class EnvironmentType(str, Enum):
    NEST = "nest"
    COMMUNITY = "community"
    HOUSE = "house"
    LOWER = "lower"
    UPPER = "upper"
    ADOLESCENCE = "adolescence"
    HIGH = "HIGH"

class RoleType(str, Enum):
    ADMINISTRATOR = "administrator"
    GUIDE = "guide"
    ASSISTANT = "assistant"
    LEARNER = "learner"
    SPONSOR = "sponsor"
    
class AreaType(str, Enum):
    PRACTICAL_LIFE = "practical_life"
    SENSORIAL = "sensorial"
    LANGUAGE = "language"
    MATHEMATICS = "mathematics"
    CULTURAL = "cultural"
    SCIENCE = "science"
    GEOGRAPHY = "geography"
    HISTORY = "history"
    COSMIC_EDUCATION = "cosmic_education"
    ART = "art"
    MUSIC = "music"
    EMOTIONAL_EDUCATION = "emotional_education"
    MOVEMENT = "movement"
    READING_WRITING = "reading_writing"
    SOCIAL_STUDIES = "social_studies"
    ECOLOGY = "ecology"
    TECHNOLOGY = "technology"
    SECOND_LANGUAGE = "second_language"
    PEACE_EDUCATION = "peace_education"

class MaterialStatus(str, Enum):
    IN_USE = "in_use"
    UNDER_REPAIR = "under_repair"
    DAMAGED = "damaged"
    INCOMPLETE = "incomplete"
    LOST = "lost"
    STORED = "stored"
    BEING_CLEANED = "being_cleaned"
    UNAVAILABLE = "unavailable"

class ActivityType(str, Enum):
    PRESENTATION = "presentation"
    WORK = "work"

class LessonType(str, Enum):
    FIRST_TIME = "first_time"
    SECOND_TIME = "second_time"
    THIRD_TIME = "third_time"

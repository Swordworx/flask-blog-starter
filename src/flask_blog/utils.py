from .database import db
from .models import Tag
from .constants import TAG_DELIMITER


def find_or_create_tags(tag_names):
    split_tags = tag_names.split(TAG_DELIMITER)
    cleaned_tags = [s.strip() for s in split_tags]
    non_empty_tags = [s for s in cleaned_tags if s != '']
    tags = []
    for tag_name in non_empty_tags:
        tag = Tag.query.filter(Tag.name == tag_name).first()
        if not tag:
            name = tag_name.lower()
            new_tag = Tag(name=name)
            db.session.add(new_tag)
            tags.append(new_tag)
        else:
            tags.append(tag)
    return tags


def tags_to_string(tags):
    tag_names = []
    for tag in tags:
        tag_names.append(tag.name)
    return f'{TAG_DELIMITER} '.join(tag_names)

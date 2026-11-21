"""Tests for image search result deduplication."""

import unittest

from vibe_framework.skills.image_providers import (
    ImageLicense,
    ImageResult,
)
from vibe_framework.skills.image_search import ImageSearchSkill


def _image(url: str, source_url: str) -> ImageResult:
    return ImageResult(
        url=url,
        thumbnail_url=url,
        width=736,
        height=1000,
        source="pinterest",
        source_url=source_url,
        author="author",
        author_url="https://www.pinterest.com/author/",
        license=ImageLicense.UNKNOWN,
        provider="pinterest",
        title="title",
    )


class TestImageSearchDeduplication(unittest.TestCase):
    def setUp(self):
        self.skill = ImageSearchSkill()

    def test_distinct_pinterest_images_are_not_deduplicated(self):
        images = [
            _image(
                "https://i.pinimg.com/originals/aa/aa/aa/first.jpg",
                "https://www.pinterest.com/pin/first/",
            ),
            _image(
                "https://i.pinimg.com/originals/bb/bb/bb/second.jpg",
                "https://www.pinterest.com/pin/second/",
            ),
        ]

        self.assertEqual(len(self.skill._deduplicate(images)), 2)

    def test_exact_duplicate_is_deduplicated(self):
        image = _image(
            "https://i.pinimg.com/originals/aa/aa/aa/first.jpg",
            "https://www.pinterest.com/pin/first/",
        )

        self.assertEqual(len(self.skill._deduplicate([image, image])), 1)

    def test_pinterest_size_variants_are_deduplicated(self):
        images = [
            _image(
                "https://i.pinimg.com/originals/aa/aa/aa/first.jpg",
                "https://www.pinterest.com/pin/first/",
            ),
            _image(
                "https://i.pinimg.com/736x/aa/aa/aa/first.jpg",
                "https://www.pinterest.com/pin/first/",
            ),
        ]

        self.assertEqual(len(self.skill._deduplicate(images)), 1)


if __name__ == "__main__":
    unittest.main()

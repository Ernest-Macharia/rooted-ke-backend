import json
import re

from django import forms
from django.core.exceptions import ValidationError


BULLET_PREFIX_RE = re.compile(r"^[-*\u2022]\s*")


class JsonStringListFormField(forms.Field):
    """Friendly admin input for JSON string arrays.

    Supports either:
    1) one item per line
    2) comma-separated values
    3) raw JSON list (for advanced users)
    """

    default_error_messages = {
        'invalid': 'Enter one item per line, comma-separated text, or a valid JSON array.',
        'invalid_item': 'Each entry must be plain text (not an object).',
    }

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('required', False)
        kwargs.setdefault(
            'widget',
            forms.Textarea(
                attrs={
                    'rows': 5,
                    'placeholder': 'One item per line (or paste a JSON array).',
                }
            ),
        )
        super().__init__(*args, **kwargs)

    def prepare_value(self, value):
        if isinstance(value, list):
            prepared = []
            for item in value:
                if isinstance(item, str):
                    prepared.append(item)
                else:
                    prepared.append(json.dumps(item, ensure_ascii=True))
            return "\n".join(prepared)
        return value

    def to_python(self, value):
        if value in self.empty_values:
            return []

        if isinstance(value, list):
            return self._normalize_list(value)

        raw = str(value).strip()
        if not raw:
            return []

        # If it looks like JSON, parse as JSON first.
        if raw[0] in '[{':
            try:
                parsed = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise ValidationError(self.error_messages['invalid']) from exc

            if isinstance(parsed, list):
                return self._normalize_list(parsed)
            raise ValidationError(self.error_messages['invalid'])

        # Friendly text input mode.
        if '\n' in raw:
            parts = raw.splitlines()
        elif ',' in raw:
            parts = raw.split(',')
        else:
            parts = [raw]

        cleaned = []
        for part in parts:
            token = BULLET_PREFIX_RE.sub('', str(part)).strip()
            if token:
                cleaned.append(token)
        return cleaned

    def _normalize_list(self, values):
        cleaned = []
        for item in values:
            if isinstance(item, (dict, list)):
                raise ValidationError(self.error_messages['invalid_item'])
            token = str(item).strip()
            if token:
                cleaned.append(token)
        return cleaned


class BlogBodyBlocksFormField(forms.Field):
    """Friendly admin input for blog body blocks.

    Preferred syntax:
      intro | Opening paragraph text
      h2    | Section heading
      p     | Standard paragraph
      tip   | Insider tip text

    Also accepts a valid JSON list of objects.
    """

    default_error_messages = {
        'invalid': 'Use one block per line as "type | text" or provide a valid JSON array of objects.',
        'invalid_item': 'Each JSON block must be an object with "type" and "text".',
    }

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('required', False)
        kwargs.setdefault(
            'widget',
            forms.Textarea(
                attrs={
                    'rows': 12,
                    'placeholder': 'intro | Intro paragraph\nh2 | Why visit\np | Main paragraph\ntip | Useful local tip',
                }
            ),
        )
        super().__init__(*args, **kwargs)

    def prepare_value(self, value):
        if isinstance(value, list):
            lines = []
            for block in value:
                if isinstance(block, dict):
                    block_type = str(block.get('type', 'p')).strip() or 'p'
                    text = str(block.get('text', '')).strip()
                    if text:
                        lines.append(f'{block_type} | {text}')
                else:
                    token = str(block).strip()
                    if token:
                        lines.append(f'p | {token}')
            return "\n".join(lines)
        return value

    def to_python(self, value):
        if value in self.empty_values:
            return []

        if isinstance(value, list):
            return self._normalize_blocks(value)

        raw = str(value).strip()
        if not raw:
            return []

        if raw[0] in '[{':
            try:
                parsed = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise ValidationError(self.error_messages['invalid']) from exc

            if not isinstance(parsed, list):
                raise ValidationError(self.error_messages['invalid'])
            return self._normalize_blocks(parsed)

        blocks = []
        for line in raw.splitlines():
            stripped = line.strip()
            if not stripped:
                continue

            if '|' in stripped:
                block_type, text = stripped.split('|', 1)
            else:
                # Plain text lines default to paragraph blocks.
                block_type, text = 'p', stripped

            normalized_type = str(block_type).strip() or 'p'
            normalized_text = str(text).strip()
            if normalized_text:
                blocks.append({'type': normalized_type, 'text': normalized_text})

        return blocks

    def _normalize_blocks(self, blocks):
        normalized = []
        for block in blocks:
            if not isinstance(block, dict):
                raise ValidationError(self.error_messages['invalid_item'])

            block_type = str(block.get('type', 'p')).strip() or 'p'
            text = str(block.get('text', '')).strip()
            if text:
                normalized.append({'type': block_type, 'text': text})

        return normalized


class PackageTiersFormField(forms.Field):
    """Friendly admin input for package pricing tiers.

    Preferred syntax per line:
      name | price | note
    Example:
      Budget | KES 25,000 | Shared transport
    """

    default_error_messages = {
        'invalid': 'Use one tier per line as "name | price | note" or provide a valid JSON array.',
        'invalid_item': 'Each tier must include at least "name" and "price".',
    }

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('required', False)
        kwargs.setdefault(
            'widget',
            forms.Textarea(
                attrs={
                    'rows': 6,
                    'placeholder': 'Budget | KES 25,000 | Shared transport\nMid | KES 42,000 | Hotel included\nPremium | KES 75,000 | Private guide',
                }
            ),
        )
        super().__init__(*args, **kwargs)

    def prepare_value(self, value):
        if isinstance(value, list):
            lines = []
            for item in value:
                if not isinstance(item, dict):
                    continue
                name = str(item.get('name', '')).strip()
                price = str(item.get('price', '')).strip()
                note = str(item.get('note', '')).strip()
                if not name and not price:
                    continue
                if note:
                    lines.append(f'{name} | {price} | {note}')
                else:
                    lines.append(f'{name} | {price}')
            return "\n".join(lines)
        return value

    def to_python(self, value):
        if value in self.empty_values:
            return []

        if isinstance(value, list):
            return self._normalize(value)

        raw = str(value).strip()
        if not raw:
            return []

        if raw[0] in '[{':
            try:
                parsed = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise ValidationError(self.error_messages['invalid']) from exc

            if not isinstance(parsed, list):
                raise ValidationError(self.error_messages['invalid'])
            return self._normalize(parsed)

        tiers = []
        for line in raw.splitlines():
            stripped = line.strip()
            if not stripped:
                continue

            parts = [part.strip() for part in stripped.split('|')]
            if len(parts) < 2:
                raise ValidationError(self.error_messages['invalid'])

            name = parts[0]
            price = parts[1]
            note = '|'.join(parts[2:]).strip() if len(parts) > 2 else ''

            if not name or not price:
                raise ValidationError(self.error_messages['invalid_item'])

            item = {'name': name, 'price': price}
            if note:
                item['note'] = note
            tiers.append(item)

        return tiers

    def _normalize(self, values):
        normalized = []
        for item in values:
            if not isinstance(item, dict):
                raise ValidationError(self.error_messages['invalid_item'])

            name = str(item.get('name', '')).strip()
            price = str(item.get('price', '')).strip()
            note = str(item.get('note', '')).strip()
            if not name or not price:
                raise ValidationError(self.error_messages['invalid_item'])

            row = {'name': name, 'price': price}
            if note:
                row['note'] = note
            normalized.append(row)
        return normalized

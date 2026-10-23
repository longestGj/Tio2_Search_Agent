"""Count visible email text with Mail Group SOP v1.1 whitespace semantics."""
import argparse
import json
from pathlib import Path


def count_mail(data):
    if not isinstance(data, dict):
        raise ValueError('input must be an object')
    if data.get('stage') not in ('Mail 1', 'Mail 2', 'Mail 3', 'Mail 4', 'reply'):
        raise ValueError('stage must be Mail 1, Mail 2, Mail 3, Mail 4 or reply')
    fields = ('subject', 'greeting', 'body', 'closing', 'signature')
    if any(not isinstance(data.get(key), str) for key in fields):
        raise ValueError('subject, greeting, body, closing and signature must be strings')
    if not data['body'].strip():
        raise ValueError('body must contain visible text')
    counts = {key: len(data[key].split()) for key in fields}
    return {
        'body_words': counts['body'],
        'full_words': sum(counts.values()),
        'mail2_within_limit': counts['body'] <= 90 if data['stage'] == 'Mail 2' else None,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', help='UTF-8 JSON containing plain visible email fields')
    args = parser.parse_args()
    try:
        result = count_mail(json.loads(Path(args.input).read_text(encoding='utf-8-sig')))
    except (OSError, UnicodeError, ValueError) as error:
        print(json.dumps({'error': str(error)}, ensure_ascii=False))
        return 2
    print(json.dumps(result, ensure_ascii=False))
    return 1 if result['mail2_within_limit'] is False else 0


if __name__ == '__main__':
    raise SystemExit(main())

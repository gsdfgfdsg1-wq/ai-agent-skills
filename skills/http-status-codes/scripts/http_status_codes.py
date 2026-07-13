#!/usr/bin/env python3
"""Look up common HTTP response status codes without external dependencies."""

import argparse
import json
import sys

STATUS_CODES = {
    100: ("Continue", "Informational", "The server received the request headers and the client should continue."),
    101: ("Switching Protocols", "Informational", "The server is changing protocols as requested."),
    200: ("OK", "Success", "The request succeeded."),
    201: ("Created", "Success", "The request created a new resource."),
    202: ("Accepted", "Success", "The request was accepted for processing."),
    204: ("No Content", "Success", "The request succeeded and there is no response body."),
    206: ("Partial Content", "Success", "The server is returning part of the requested resource."),
    300: ("Multiple Choices", "Redirection", "The request has more than one possible response."),
    301: ("Moved Permanently", "Redirection", "The resource has a permanent new URL."),
    302: ("Found", "Redirection", "The resource is temporarily available at another URL."),
    303: ("See Other", "Redirection", "The response can be found at a different URL using GET."),
    304: ("Not Modified", "Redirection", "The cached resource is still valid."),
    307: ("Temporary Redirect", "Redirection", "Repeat the request at another URL without changing its method."),
    308: ("Permanent Redirect", "Redirection", "Repeat future requests at another URL without changing their method."),
    400: ("Bad Request", "Client Error", "The server cannot process the request because it is invalid."),
    401: ("Unauthorized", "Client Error", "Authentication is required to access the resource."),
    403: ("Forbidden", "Client Error", "The server refuses to authorize the request."),
    404: ("Not Found", "Client Error", "The server cannot find the requested resource."),
    405: ("Method Not Allowed", "Client Error", "The request method is not allowed for this resource."),
    406: ("Not Acceptable", "Client Error", "The server cannot produce an acceptable response representation."),
    408: ("Request Timeout", "Client Error", "The server timed out while waiting for the request."),
    409: ("Conflict", "Client Error", "The request conflicts with the current resource state."),
    410: ("Gone", "Client Error", "The resource is permanently unavailable."),
    413: ("Content Too Large", "Client Error", "The request content is larger than the server allows."),
    415: ("Unsupported Media Type", "Client Error", "The request content type is not supported."),
    418: ("I'm a teapot", "Client Error", "The server refuses to brew coffee because it is a teapot."),
    422: ("Unprocessable Content", "Client Error", "The request syntax is valid but its instructions cannot be processed."),
    429: ("Too Many Requests", "Client Error", "The client sent too many requests in a period of time."),
    500: ("Internal Server Error", "Server Error", "The server encountered an unexpected condition."),
    501: ("Not Implemented", "Server Error", "The server does not support the required functionality."),
    502: ("Bad Gateway", "Server Error", "The server received an invalid response from an upstream server."),
    503: ("Service Unavailable", "Server Error", "The server is temporarily unable to handle the request."),
    504: ("Gateway Timeout", "Server Error", "An upstream server did not respond in time."),
    505: ("HTTP Version Not Supported", "Server Error", "The server does not support the HTTP version used in the request."),
}

CATEGORIES = {
    "1xx": "Informational",
    "2xx": "Success",
    "3xx": "Redirection",
    "4xx": "Client Error",
    "5xx": "Server Error",
}


def record(code, data):
    phrase, category, description = data
    return {"code": code, "phrase": phrase, "category": category, "description": description}


def parse_category(value):
    normalized = value.lower().replace(" ", "")
    aliases = {"1": "1xx", "2": "2xx", "3": "3xx", "4": "4xx", "5": "5xx"}
    normalized = aliases.get(normalized, normalized)
    if normalized not in CATEGORIES:
        raise ValueError("category must be one of: 1xx, 2xx, 3xx, 4xx, 5xx")
    return normalized


def format_text(results):
    if not results:
        return "No matching HTTP status codes found."
    lines = []
    for item in results:
        lines.append(f"{item['code']} {item['phrase']} ({item['category']})")
        lines.append(f"  {item['description']}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Look up common HTTP response status codes.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--code", type=int, help="look up one numeric status code")
    group.add_argument("--category", help="list a status category: 1xx through 5xx")
    group.add_argument("--search", help="search code phrases, categories, and descriptions")
    parser.add_argument("--json", action="store_true", help="write structured JSON output")
    args = parser.parse_args()

    if args.code is not None:
        results = [record(args.code, STATUS_CODES[args.code])] if args.code in STATUS_CODES else []
    elif args.category:
        try:
            prefix = parse_category(args.category)[0]
        except ValueError as error:
            parser.error(str(error))
        results = [record(code, data) for code, data in STATUS_CODES.items() if str(code).startswith(prefix)]
    elif args.search:
        query = args.search.casefold()
        results = [
            record(code, data)
            for code, data in STATUS_CODES.items()
            if query in str(code) or query in " ".join(data).casefold()
        ]
    else:
        results = [record(code, data) for code, data in STATUS_CODES.items()]

    results.sort(key=lambda item: item["code"])
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print(format_text(results))
    return 0 if results else 1


if __name__ == "__main__":
    sys.exit(main())

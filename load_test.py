"""Simple load test script using asyncio + aiohttp.

Usage:
  python load_test.py https://your-site.web.app/ 4000

This will send `concurrency` simultaneous GET requests to the given URL and report successes/failures.

Notes:
- This is a basic tool for local sanity-checking. For more advanced load testing, consider k6, locust, or Apache JMeter.
"""

import asyncio
import sys
import time

import aiohttp


async def fetch(session: aiohttp.ClientSession, url: str) -> bool:
    try:
        async with session.get(url, timeout=10) as resp:
            return resp.status == 200
    except Exception:
        return False


async def run(url: str, concurrency: int):
    connector = aiohttp.TCPConnector(limit=concurrency)
    timeout = aiohttp.ClientTimeout(total=20)
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        tasks = [fetch(session, url) for _ in range(concurrency)]
        results = await asyncio.gather(*tasks)
        return results


def main():
    if len(sys.argv) < 3:
        print("Usage: python load_test.py <url> <concurrency>")
        sys.exit(1)

    url = sys.argv[1]
    try:
        concurrency = int(sys.argv[2])
    except ValueError:
        print("concurrency must be an integer")
        sys.exit(1)

    start = time.time()
    results = asyncio.run(run(url, concurrency))
    elapsed = time.time() - start

    success = sum(1 for r in results if r)
    fail = len(results) - success

    print(f"URL: {url}")
    print(f"Concurrency: {concurrency}")
    print(f"Elapsed: {elapsed:.1f}s")
    print(f"Success: {success}  Fail: {fail}")


if __name__ == "__main__":
    main()

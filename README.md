# Python Web Scanner

[`TheCrawlerFinal.py`](TheCrawlerFinal.py) is an interactive Python web crawler and asset downloader. Give it a domain, and it follows links found in the site's HTML, downloads supported documents, images, and archives, and writes text reports for other asset links, external links, and failed downloads.

## Setup

Install Python 3 and Git, then clone the repository.

```sh
git clone https://github.com/N0C7URNUS/Python-Web-Scanner.git
cd Python-Web-Scanner
```

Create a virtual environment and install Requests and Beautiful Soup.

**Linux**

```sh
python3 -m venv .venv
.venv/bin/python -m pip install requests beautifulsoup4
```

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install requests beautifulsoup4
```

## Usage

- **Linux** — `.venv/bin/python TheCrawlerFinal.py`
- **Windows PowerShell** — `.\.venv\Scripts\python.exe TheCrawlerFinal.py`

At the prompt, enter a bare domain such as `example.com`. Use a site you own or have permission to crawl. The script builds an `http://` URL from the domain and follows any redirects, including an upgrade to HTTPS if the site provides one.

## Output

The script saves downloads and reports under `~/Documents/<domain>/` in your home directory. The paths below are relative to that folder.

| Contents | Path |
| --- | --- |
| Downloaded documents, such as PDFs and CSVs | `<domain>-Docs/` |
| Downloaded images, such as PNGs and JPEGs | `<domain>-Images/` |
| Downloaded archives, such as ZIP and TAR files | `<domain>-Archives/` |
| Audio URLs | `<domain>-Audio/Audio_Links_File.txt` |
| Video URLs | `<domain>-Videos/Video_Links_File.txt` |
| URLs for scripts, stylesheets, and structured data | `<domain>-Code/Code_Links_File.txt` |
| External URLs discovered in the HTML | `External_Links_File.txt` |
| Asset URLs whose downloads failed | `Failed_Downloads_Links_File.txt` |

Each run appends to existing text reports. Downloads that resolve to the same filename in the same folder can overwrite one another.

## How the crawler works

- Requests fetches pages through a shared session, and Beautiful Soup extracts URLs from supported HTML tags. Supported URL forms include absolute URLs, protocol-relative URLs such as `//example.com/image.png`, and paths beginning with `/`. Plain relative paths such as `images/logo.png` and links added by JavaScript after page load are skipped.
- The crawler matches the host and port exactly as written in the resolved starting URL. It reports external links and queues matching URLs that have no recognized asset extension. HTTP redirects can still lead to another host.
- Asset categories are based on the final extension in each URL path. Downloads are streamed to disk after the crawl finishes. The pending queue holds up to 5,000 URLs at a time, and each asset or report set managed by the script's capacity check holds up to 2,500 entries.

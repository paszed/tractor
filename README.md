# 🚜 Tractor

Tractor is a simple CLI tool to extract structured data from websites.

## 💡 Idea

Turn messy web pages into clean datasets.

URL → extract items → map fields → output JSON / CSV

## 🚧 Status

Early development.

This repo is just initialized. Nothing is implemented yet.

## 🧭 Direction

Tractor focuses on quick, real-world scraping tasks:

- input: URL
- extract: repeating items (listings)
- fields: title, price, link (extendable)
- output: JSON or CSV

No crawling. No browser automation. No framework.

## ⚙️ Philosophy

- Simple > complete
- Fast > perfect
- CLI-first
- Do one thing well

## 🧪 Usage (planned)

tractor <url> --selector ".item"

tractor scrape config.json

## 🚫 Scope

Not included:

- authentication
- anti-bot handling
- complex pagination
- dashboards / UI

## 🎯 Why

Existing tools are either too heavy or too low-level.

Tractor aims to be the fastest way to go from:

website → usable data

## 📄 License

MIT

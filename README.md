<p align="center">
  <img src="img/cabe_github%20autobackup.png" alt="Auto Backup" width="800">
</p>


# Auto Backup

Lightweight Windows utility for automatic rolling ZIP backups with FIFO retention and permanent manual snapshots.

## Features

- Automatic ZIP backups at configurable intervals
- FIFO retention for automatic backups
- Permanent manual snapshots
- Separate `Auto` and `Manual` backup folders
- Optional description for manual snapshots
- Simple CustomTkinter interface
- Visual countdown until the next automatic backup

## Requirements

- Python 3
- customtkinter
- Pillow

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Run

```bash
python auto_backup_v15.py
```

## Backup structure

```text
Destination/
├── Auto/
│   ├── Backup_YYYY-MM-DD_HH-MM-SS.zip
│   └── ...
└── Manual/
    ├── Backup_YYYY-MM-DD_HH-MM-SS.zip
    └── Backup_YYYY-MM-DD_HH-MM-SS_description.zip
```

Automatic backups are rotated according to the configured number of copies to keep.

Manual snapshots are preserved permanently unless deleted manually.

## Version

Current version: **v1.5**

## License

See `LICENSE`.

---

Corrosion Labs

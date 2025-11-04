from django.db import migrations, models
from django.conf import settings

def forwards_func(apps, schema_editor):
    import os
    from pathlib import Path
    try:
        import pwd
        import grp
    except Exception:  # pragma: no cover
        pwd = None
        grp = None

    base = Path(settings.BASE_DIR) / "persistent"
    db_dir = base / "db"
    media_dir = base / "media"
    db_path = db_dir / "db.sqlite3"

    # Ensure directories exist
    db_dir.mkdir(parents=True, exist_ok=True)
    media_dir.mkdir(parents=True, exist_ok=True)

    # Relax permissions to allow write (group write enabled)
    try:
        os.chmod(base, 0o775)
    except Exception:
        pass
    try:
        os.chmod(db_dir, 0o775)
    except Exception:
        pass
    try:
        os.chmod(media_dir, 0o775)
    except Exception:
        pass

    # If database file already created by migrate, ensure its permissions
    if db_path.exists():
        try:
            os.chmod(db_path, 0o664)
        except Exception:
            pass

    # Try to chown to appuser if exists (inside container)
    try:
        if pwd and grp:
            uid = pwd.getpwnam("appuser").pw_uid
            gid = grp.getgrnam("appuser").gr_gid
            for p in [base, db_dir, media_dir, db_path]:
                try:
                    if p.exists():
                        os.chown(p, uid, gid)
                except Exception:
                    # If chown fails (e.g., not running as root), ignore
                    pass
    except KeyError:
        # appuser not found (e.g., local dev); ignore
        pass


def backwards_func(apps, schema_editor):
    # No-op: we do not remove directories or revert permissions on rollback
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(forwards_func, backwards_func),
    ]

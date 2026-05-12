# Renum Wiki 
# ==========
#
# Rename any markdown filename in ``wiki/`` that starts with a
# **1-digit number** followed by an underscore by **prefixing a 0**
# to the number.
#
# **Examples:**
#
# - ``7_alembic.md`` → ``07_alembic.md``
# - ``9_conn_pass.md`` → ``09_conn_pass.md``
#
# **Keep unchanged:**
#
# - ``11_scheduler.md`` → ``11_scheduler.md``
# - ``10_celery.md`` → ``10_celery.md``
#
# ----   
#   
# ::

from pathlib import Path

wiki_dir = Path(".")
count = 0

for path in wiki_dir.iterdir():
    if (
        path.is_file()
        and path.suffix == ".md"
        and len(path.name) >= 3
        and path.name[0].isdigit()
        and path.name[1] == "_"
    ):
        new_name = f"0{path.name}"
        path.rename(path.with_name(new_name))
        count += 1
        print("- " + new_name)

print(f"= {count} file(s) renamed")
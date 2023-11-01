from invoke import task

# Sphinx: https://www.sphinx-doc.org/en/master/usage/quickstart.html

@task
def rst(ctx):
	ctx.run("pylit -c cmp_folders.py cmp_folders.py.rst")

@task
def py(ctx):
	ctx.run("pylit -t cmp_folders.py.rst cmp_folders.py")

@task
def lit(ctx):
	ctx.run(f"make html")

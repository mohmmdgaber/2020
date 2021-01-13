from manager.managerpages import workers,managers,products

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, managers=managers, workers=workers,products=products)

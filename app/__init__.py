from app import app, bundles

if __name__ == "__main__":
    for bundle in bundles:
        bundle.build()
    app.run()

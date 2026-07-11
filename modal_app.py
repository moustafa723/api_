import modal

image = (
    modal.Image.debian_slim()
    .add_local_dir(".", remote_path="/root")
    .pip_install_from_requirements("requirements.txt")
)

app = modal.App("surgenius-api")


@app.function(image=image)
@modal.asgi_app()
def fastapi_app():
    from app import app
    return app
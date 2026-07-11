import modal

image = (
    modal.Image.debian_slim()
    .pip_install_from_requirements("requirements.txt")
)

app = modal.App("surgenius-api")


@app.function(image=image)
@modal.asgi_app()
def fastapi_app():
    from app import app as fastapi_app
    return fastapi_app
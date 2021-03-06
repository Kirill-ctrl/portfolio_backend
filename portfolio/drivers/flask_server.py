from typing import Optional, List

from flask import Flask, Blueprint


class FlaskServer:

    _app = Flask(__name__)

    @classmethod
    def get_app(cls):
        return cls._app

    @classmethod
    def set_config(cls, upload_folder: str, max_content_length: int):
        cls._app.config['UPLOAD_FOLDER'] = upload_folder
        cls._app.config['MAX_CONTENT_LENGTH'] = max_content_length

    @classmethod
    def set_api(cls, apis: List[Blueprint] or Blueprint):
        for api in apis:
            print(api.name)
            if api.name == 'main':
                cls._app.register_blueprint(api, url_prefix='/')
            else:
                cls._app.register_blueprint(api, url_prefix=f"/{api.name}")

    @classmethod
    def run_server(cls, host: str, port: int, debug: bool):
        cls._app.run(
            host=host,
            port=port,
            debug=debug,
            load_dotenv=False
        )

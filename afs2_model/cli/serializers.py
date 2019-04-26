from pathlib import Path

from afs2_model import AFSClient

ROOT_PATH = Path.home().joinpath(".eipaas")
ROOT_PATH.mkdir(exist_ok=True)
CONFIG_PATH = ROOT_PATH.joinpath("config.json")


class AFSClientSerializer:
    @staticmethod
    def serialization(afs_client, instance=None, dumps=None, loads=None):
        if not dumps:
            from json import dumps, loads

        try:
            with CONFIG_PATH.open() as f:
                state = loads(f.read())
        except:
            state = {}

        state.update(
            {
                "api_endpoint": getattr(afs_client, "api_endpoint", None),
                "api_version": getattr(afs_client, "api_version", None),
            }
        )

        session = getattr(afs_client, "_session", None)
        if session:
            state.update(
                {
                    "ssl": getattr(session, "verify", True),
                    "token": getattr(session, "token", None),
                }
            )

        if instance:
            state.update({"instance_id": instance.uuid})

        with CONFIG_PATH.open("w") as f:
            f.write(dumps(state, indent=4))

        return True

    @staticmethod
    def deserialization(loads=None):
        if not loads:
            from json import loads

        try:
            with CONFIG_PATH.open() as f:
                state = loads(f.read())
        except:
            state = {}

        return state

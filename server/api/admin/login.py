from flask_jwt_simple import create_jwt, jwt_required, get_jwt_identity
from flask_restplus import Resource, Namespace, reqparse
import hashlib
from utils import Config, logger

ns_admin_login = Namespace("admin/login", description="로그인")

parser = ns_admin_login.parser()
parser.add_argument(
    "Authorization",
    type=str,
    location="headers",
    help="Bearer jwt token",
    required=True,
)


@ns_admin_login.route("/")
class Login(Resource):
    @ns_admin_login.doc("로그인하기", params={"username": "id", "password": "password"})
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, help="username")
        parser.add_argument("password", type=str, help="password")
        args = parser.parse_args(strict=True)

        def _validate(args):
            username = args.get("username")
            password = args.get("password")
            up = username + password

            logger.info(f"Authorizing with {Config.LOGIN_TOKEN}")
            if hashlib.sha256(up.encode()).hexdigest() != Config.LOGIN_TOKEN:
                return False

            return True

        if not _validate(args):
            return {}, 401

        ret = {"jwt": create_jwt(identity=args["username"])}
        return ret, 200

    @ns_admin_login.doc(
        "로그인 테스트",
        params={"username": "username", "password": "password"},
        parser=parser,
    )
    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, help="username")
        parser.add_argument("password", type=str, help="password")
        args = parser.parse_args(strict=True)

        def _validate_args(args):
            pass

        _validate_args(args)
        return {"username": get_jwt_identity()}, 200

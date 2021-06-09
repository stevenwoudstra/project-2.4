from pprint import pprint
import requests
from flask import Blueprint, Response, request

# A list of routes that keeps track which urls are accessible from a local viewpoint. Whether a request is through a
# local viewpoint is defined by whether or not it is sent by the Main-API, which adds a special header to the request,
# namely Public-Request.

WHITELIST = []
UNPROTECTED = []


class AuthBlueprint(Blueprint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.url_prefix is None:
            self.url_prefix = ""

    def route(self, rule, public=True, protected=True, **options):
        """
        Override of Blueprint::route. It registers the route to the WHITELIST if the public param is set to True
        :param rule: Route to add to the WHITELIST
        :param public: Whether or not the route should be whitelisted
        :param protected: Wheter or not the route should require authentication
        :param options: Other options that are available for Blueprint::route
        :return:
        """
        if public:
            # Include the full url trail for convenience
            WHITELIST.append(self.url_prefix + rule)
        if not protected:
            UNPROTECTED.append(self.url_prefix + rule)
        return super().route(rule, **options)


class AuthMiddleWare:
    """
    This middleware checks if a request came from the Main API. If so, it is only allowed to go get responses from
    routes that are registered on the WHITELIST.
    """

    def __init__(self, app):
        self.__app = app

    def __call__(self, environ, start_response):
        # Check if request came from Main API
        public_request = (
            "HTTP_PUBLIC_REQUEST" in environ or "HTTPS_PUBLIC_REQUEST" in environ
        )
        if public_request and environ["PATH_INFO"] not in WHITELIST:
            # Send a forbidden response if the route is not on the whitelist
            res = Response(
                u"This route is not in the whitelist", mimetype="text/plain", status=403
            )
            return res(environ, start_response)
        if public_request and environ["PATH_INFO"] not in UNPROTECTED:
            try:
                user_id = self.authenticate(
                    {"Authorization": environ["HTTP_AUTHORIZATION"]}
                )
            except KeyError:
                user_id = None
            print(user_id)
            if user_id is None:
                # Send a forbidden response if the route is not on the whitelist
                res = Response(
                    u"You are not authorised", mimetype="text/plain", status=401
                )
                return res(environ, start_response)
            environ["user_id"] = user_id
        if (
            not public_request
            and environ["PATH_INFO"] not in UNPROTECTED
            and "HTTP_AUTH_USER_ID" in environ
        ):

            environ["user_id"] = int(environ["HTTP_AUTH_USER_ID"])

        return self.__app(environ, start_response)

    @staticmethod
    def authenticate(headers):
        try:
            req = requests.post("/verify_jwt", headers=headers)
            if req.status_code == 200:
                response = req.json()
                if "user_id" in response:
                    return response["user_id"]
            else:
                print("failed to authenticate. Reason:", req.status_code, req.content)
        except Exception as e:
            return None
        return None

# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2014-11-20 10:57:52
#    email     :   fengidri@yeah.net
#    version   :   1.0.1
class BottleException(Exception):
    """ A base class for exceptions used by bottle. """
    pass

class RouteError(BottleException):
    """ This is a base class for all routing related exceptions """


class RouteReset(BottleException):
    """ If raised by a plugin or request handler, the route is reset and all
        plugins are re-applied. """

class RouterUnknownModeError(RouteError): pass


class RouteSyntaxError(RouteError):
    """ The route parser found something not supported by this router. """


class RouteBuildError(RouteError):
    """ The route could not be built. """

if __name__ == "__main__":
    pass

